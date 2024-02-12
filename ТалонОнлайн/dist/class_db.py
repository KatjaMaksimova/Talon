from hashlib import md5
from DataUserSave import DataUserSave
import sqlite3


class EmailError(Exception):  # исключение
    pass


class DataBase:
    """Работа с базой данных"""
    def __init__(self):
        self.db_name = "db/db.db"

    def new_talon(self, doctor, data, time):  # добавление талона
        con = sqlite3.connect(self.db_name)
        try:
            cur = con.cursor()
            talon = con.execute(f"""
                    SELECT id FROM talons
                    WHERE time = '{time}' AND data = '{data}' AND doctor = {doctor}
                    """).fetchone()
            assert not talon
            cur.execute(f"""
                                INSERT INTO talons (doctor, data, time)
                                VALUES('{doctor}', '{data}', '{time}')""")
            con.commit()
            return True
        except AssertionError:
            return False

    def login_auto_user(self):  # возвращение данных из базы данных
        dus = DataUserSave()
        try:
            email, password = dus.email_and_password()
            assert email and password
            con = sqlite3.connect(self.db_name)
            try:
                res = list(con.execute(f"""
                SELECT * FROM users
                WHERE email = '{email}'
                 """).fetchone())
                if res:
                    return ["user", res]
                else:
                    res = list(con.execute(f"""
                            SELECT * FROM doctors
                            WHERE email = '{email}'
                             """).fetchone())
                    assert res
                    return ["doctor", res]
            except:
                res = list(con.execute(f"""
                            SELECT * FROM doctors
                            WHERE email = '{email}'
                            """).fetchone())
                assert res
                return ["doctor", res]
        except (AssertionError, Exception):
            dus.close_user()
            return []

    def registration_user(self, name=None, medical_card=None, password=None, email=None, info=None):
        # регистрация пользователя
        con = sqlite3.connect(self.db_name)

        emails = con.execute(f"""
        SELECT id FROM users
        WHERE email = '{email}'
        """).fetchone()

        if emails:
            raise EmailError("Такой email уже есть")

        cur = con.cursor()
        med_id = con.execute(f"""
SELECT id_medical_card FROM medical_cards
WHERE id_medical_card = '{medical_card}'
 """).fetchone()
        assert not med_id
        cur.execute(f"""
                    INSERT INTO medical_cards (id_medical_card, info_of_user)
                    VALUES('{medical_card}', '{info}')""")
        con.commit()
        id_medical_card = con.execute(f"""
SELECT id FROM medical_cards
WHERE id_medical_card = '{medical_card}'
 """).fetchone()[0]
        assert id_medical_card
        hash = md5(bytes(password.encode('utf8'))).hexdigest()
        cur.execute(f"""
                        INSERT INTO users (id_medical_card, password, email, name)
                        VALUES('{id_medical_card}', '{hash}', '{email}', '{name}')""")
        con.commit()
        dus = DataUserSave()
        dus.new_user(email, hash)

    def registration_doctor(self, name=None, email=None, password=None, profession="Врач"):  # регистрация доктора
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        profession_id = con.execute(f"""
SELECT id FROM professions
WHERE name = '{profession}'
 """).fetchone()
        assert profession_id
        profession_id = profession_id[0]
        emails = con.execute(f"""
SELECT id FROM doctors
WHERE email = '{email}'
""").fetchone()

        if emails:
            raise EmailError("Такой email уже есть")

        hash = md5(bytes(password.encode('utf8'))).hexdigest()
        cur.execute(f"""
                                INSERT INTO doctors (name, email, password, profession)
                                VALUES('{name}', '{email}', '{hash}', '{profession_id}')""")
        con.commit()
        dus = DataUserSave()
        dus.new_user(email, hash)

    def update_db(self, table, word1, word2, id_ud):  # обнавляет в заданной таблице значения по id
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        if type(word2) is str:
            cur.execute(f"""
UPDATE {table}
SET {word1} = '{word2}'
WHERE id = {id_ud}
""")
        elif type(word2) is int:
            cur.execute(f"""
            UPDATE {table}
            SET {word1} = {word2}
            WHERE id = {id_ud}
            """)
        con.commit()

    def login_user(self, email, password):  # вход пользователя
        dus = DataUserSave()
        dus.new_user(email, password)
        return self.login_auto_user()

    def search(self, table, word1, word2, res="*"):  # возвращает по базе данных
        con = sqlite3.connect(self.db_name)
        try:
            result = None
            if type(word2) is str:
                result = con.execute(f"""
                SELECT {res} FROM {table}
                WHERE {word1} = '{word2}'
                 """).fetchall()
            elif type(word2) is int:
                result = con.execute(f"""
                            SELECT {res} FROM {table}
                            WHERE {word1} = {word2}
                             """).fetchall()
            return result
        except:
            return None
