from hashlib import md5


class DataUserSave:  # класс для сохранения захэшированного пароля и почты
    def __init__(self):
        self.file_data = "data_user.txt"

    def new_user(self, email, password):  # запись почты и пароля
        with open(self.file_data, 'w', encoding='utf-8') as f:
            f.write(f"{email}\n{md5(bytes(password.encode('utf8'))).hexdigest()}")  # хэширование и запись

    def close_user(self):  # очистить файл
        with open(self.file_data, 'w', encoding='utf-8') as f:
            f.write("")

    def email_and_password(self):  # получение почты и пароля
        with open(self.file_data, "r") as f:
            email = f.readline().strip()
            password = f.readline().strip()
        return email, password

    def new_email(self, email):  # смена почты
        _, password = self.email_and_password()
        with open(self.file_data, 'w', encoding='utf-8') as f:
            f.write(f"{email}\n{password}")
