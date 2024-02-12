from class_db import *
from DataUserSave import *

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import QtCore, QtWidgets

import sys


class MyWidget(QMainWindow):  # начальное окно
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.registration)
        self.label_2.hide()
        self.checkBox.stateChanged.connect(self.show_password)

    def registration(self):  # переход на окно регистрации
        ex4.show()
        self.hide()

    def login(self):  # вход
        text_email = self.lineEdit.text()
        password_text = self.lineEdit_2.text()
        db = DataBase()
        answer = db.login_user(text_email, password_text)
        if not answer:
            self.label_2.show()
        else:
            if answer[0] == "user":
                ex2.show()
                ex2.updateTable()
                self.hide()
            elif answer[0] == "doctor":
                ex3.show()
                ex3.update_Table()
                self.hide()

    def show_password(self, state):  # кнопка для показа скрытого пароля
        if state == QtCore.Qt.Checked:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)


class MyWidget2(QMainWindow):  # главное окно пользователя
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/mainWindow.ui", self)
        self.pushButton.clicked.connect(self.profile)
        self.pushButton_2.clicked.connect(self.talons_for_users)
        self.updateTable()

    def updateTable(self):  # обновить таблицу с талонами
        try:
            db = DataBase()
            user_id = db.login_auto_user()[1][0]
            res = db.search(table="talons", word1="user", word2=user_id)
            self.tableWidget.setRowCount(len(res))
            self.tableWidget.setColumnCount(4)
            for i, elem in enumerate(res):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(elem[0])))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(
                    db.search(table="doctors", word1="id", word2=int(str(elem[1])), res="name")[0][0]))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(elem[2])))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(elem[3])))
        except IndexError:
            pass

    def talons_for_users(self):  # открытие окна для выбора талона
        ex8.show()
        self.hide()

    def profile(self):  # открытие профиля
        ex6.show()
        ex6.update()
        self.hide()


class MyWidget3(QMainWindow):  # главное окно доктора
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/mainWindowDoctor.ui", self)
        self.pushButton.clicked.connect(self.profile)
        self.pushButton_2.clicked.connect(self.graf)
        self.pushButton_3.clicked.connect(self.search)
        self.calendarWidget.activated.connect(self.update_Table)
        self.update_Table()

    def update_Table(self):  # обновление таблицы с талонами
        try:
            db = DataBase()
            data = self.calendarWidget.selectedDate().toString('dd-MM-yyyy')
            doctor = db.login_auto_user()[1][0]
            res = [i for i in db.search(table="talons", word1="data", word2=data) if i[1] == doctor]

            self.tableWidget.setRowCount(len(res))
            self.tableWidget.setColumnCount(4)
            for i, elem in enumerate(res):
                if elem[-1]:
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(str(elem[0])))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(db.search(table="users", word1="id",
                                                                              word2=int(elem[-1]), res="name")[0][0]))

                    self.tableWidget.setItem(i, 2, QTableWidgetItem(str(elem[3])))
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(
                        str(db.search(table="medical_cards", word1="id",
                                      word2=int(db.search(table="users",
                                                          word1="id",
                                                          word2=int(
                                                              elem[-1]),
                                                          res="id_medical_card")[
                                                    0][0]),
                                      res="id_medical_card")[0][0])))
                else:
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(str(elem[0])))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem("---"))
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(str(elem[3])))
                    self.tableWidget.setItem(i, 3, QTableWidgetItem("---"))


        except:
            pass

    def search(self):  # поиск карточки по id
        ex9.show()
        self.hide()

    def graf(self):  # открытие окна для установки графика
        ex7.show()
        self.hide()

    def profile(self):  # открытие профиля врача
        ex5.show()
        self.hide()


class MyWidget4(QMainWindow):  # открытие окна регистраации
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/registration.ui", self)
        self.doctor = False
        self.label_9.hide()
        self.label_10.hide()
        self.label_2.hide()
        self.label_11.hide()
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.registration)
        self.checkBox_3.stateChanged.connect(self.doctor_state)
        self.checkBox.stateChanged.connect(self.show_password)
        self.checkBox_2.stateChanged.connect(self.show_password_2)

    def login(self):  # открытие окна для входа
        ex1.show()
        self.hide()

    def doctor_state(self, state):
        self.doctor = not self.doctor
        if self.doctor:
            self.label_3.hide()
            self.lineEdit.hide()
            self.label_9.hide()
        else:
            self.label_3.show()
            self.lineEdit.show()

    def registration(self):  # регистрация
        registration_error = False
        self.label_9.hide()
        self.label_10.hide()
        self.label_2.hide()
        self.label_11.hide()
        db = DataBase()
        if self.doctor:
            if self.lineEdit_5.text():
                if db.search(table="doctors", word1="email", word2=self.lineEdit_5.text()):
                    self.label_10.show()
                    registration_error = True
            else:
                self.label_10.show()
                registration_error = True
        else:
            if self.lineEdit_5.text():
                if db.search(table="users", word1="email", word2=self.lineEdit_5.text()):
                    self.label_10.show()
                    registration_error = True
            else:
                self.label_10.show()
                registration_error = True
            if self.lineEdit.text():
                if db.search(table="medical_cards", word1="id_medical_card", word2=self.lineEdit.text()):
                    self.label_9.show()
                    registration_error = True
            else:
                self.label_9.show()
                registration_error = True
        if self.lineEdit_2.text() != self.lineEdit_4.text() or len(self.lineEdit_2.text()) < 8:
            self.label_2.show()
            registration_error = True
        if not self.lineEdit_3.text():
            self.label_11.show()
            registration_error = True

        if not registration_error:
            if self.doctor:
                db.registration_doctor(name=self.lineEdit_3.text(), email=self.lineEdit_5.text(),
                                       password=self.lineEdit_2.text())
            elif not self.doctor:
                db.registration_user(name=self.lineEdit_3.text(), email=self.lineEdit_5.text(),
                                     password=self.lineEdit_2.text(), medical_card=self.lineEdit.text())
            if db.login_auto_user():
                if self.doctor:
                    ex3.show()
                    ex3.update_Table()
                else:
                    ex2.show()
                    ex2.updateTable()
                self.hide()

    def show_password(self, state):  # показать пароль
        if state == QtCore.Qt.Checked:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

    def show_password_2(self, state):  # показать пароль
        if state == QtCore.Qt.Checked:
            self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)


class MyWidget5(QMainWindow):  # открытие окна профиля доктора
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/profileDoctor.ui", self)
        self.pushButton.clicked.connect(self.back)
        self.label_11.hide()
        self.label_10.hide()
        self.label_9.hide()
        self.pushButton_2.clicked.connect(self.redact)
        self.pushButton_3.clicked.connect(self.exit)
        try:
            db = DataBase()
            doctor = db.login_auto_user()[1]
            name = doctor[1]
            email = doctor[2]
            self.lineEdit_3.setText(name)
            self.lineEdit.setText(email)
            prof = db.search(table="professions", word1="id", word2=doctor[-1])[0]
            if prof[0] == 13:
                self.comboBox.setCurrentIndex(0)
            else:
                self.comboBox.setCurrentIndex(
                    [self.comboBox.itemText(i) for i in range(self.comboBox.count())].index(prof[1]))
        except:
            pass

    def exit(self):  # выход из профиля
        dus = DataUserSave()
        dus.close_user()
        ex1.show()
        self.hide()

    def redact(self):  # редактирование профиля
        self.label_11.hide()
        self.label_10.hide()
        self.label_9.hide()
        db = DataBase()
        doctor = db.login_auto_user()[1]
        name = self.lineEdit_3.text()
        email = self.lineEdit.text()
        prof = self.comboBox.currentText()
        prof_error = False

        if email:
            if db.search(table="doctors", word1="email", word2=email, res="id") \
                    and not db.search(table="doctors", word1="email", word2=email, res="id")[0][0] == doctor[0]:
                self.label_10.show()
                prof_error = True
            elif not db.search(table="doctors", word1="email", word2=email, res="id"):
                pass
        else:
            self.label_10.show()
            prof_error = True
        if not self.lineEdit_3.text():
            self.label_11.show()
            prof_error = True

        if self.comboBox.currentText() == "":
            self.label_9.show()
            prof_error = True
        if not prof_error:
            db.update_db(table="doctors", word1="name", word2=name, id_ud=doctor[0])
            db.update_db(table="doctors", word1="email", word2=email, id_ud=doctor[0])
            dus = DataUserSave()
            dus.new_email(email)
            id_prof = db.search(table="professions", word1="name", word2=prof)[0][0]
            db.update_db(table="doctors", word1="profession", word2=id_prof, id_ud=doctor[0])

    def back(self):  # вернуться назад
        ex3.show()
        ex3.update_Table()
        self.hide()


class MyWidget6(MyWidget):  # открытие окна профиля пользователя
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/profileUsers.ui", self)
        self.pushButton.clicked.connect(self.back)
        self.pushButton_3.clicked.connect(self.exit)
        self.pushButton_2.clicked.connect(self.redact)

        self.label_11.hide()
        self.label_10.hide()
        self.update()

    def update(self):  # обновление профиля
        try:
            db = DataBase()
            user = db.login_auto_user()[1]
            email, name = user[-2::]
            med_id, about = db.search(table="medical_cards", word1="id", word2=user[1])[0][1:]
            self.lineEdit_3.setText(name)
            self.lineEdit.setText(email)
            self.lineEdit_4.setText(str(med_id))
            self.textEdit.setText(str(about))
            self.textEdit.setReadOnly(True)
            self.lineEdit_4.setReadOnly(True)

        except:
            pass

    def redact(self):  # редактирование профиля пользователя
        self.label_11.hide()
        self.label_10.hide()
        name = self.lineEdit_3.text()
        email = self.lineEdit.text()
        error = False
        db = DataBase()
        user = db.login_auto_user()[1]
        if name:
            db.update_db(table="users", word1="name", word2=name, id_ud=user[0])
        else:
            self.label_11.show()
        if email:
            res = db.search(table="users", word1="email", word2=email, res="email")
            if res and res[0][0] == user[-2]:
                pass
            elif not res:
                db.update_db(table="users", word1="email", word2=email, id_ud=user[0])
                dus = DataUserSave()
                dus.new_email(email)
            else:
                self.label_10.show()
        else:
            self.label_10.show()

    def back(self):  # вернутся назад
        ex2.show()
        ex2.updateTable()
        self.hide()

    def exit(self):  # выход
        db = DataUserSave()
        db.close_user()
        ex1.show()
        self.hide()


class MyWidget7(MyWidget):  # открытие окна графиком работы
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/graf.ui", self)
        self.pushButton_2.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.addTalon)
        self.calendarWidget.clicked.connect(self.clik)
        self.label.hide()
        self.show_table()

    def back(self):  # назад
        ex3.show()
        ex3.update_Table()
        self.hide()

    def clik(self):  # отслеживание нажатия на календарь
        self.show_table()

    def show_table(self):  # показать таблицу с талонами
        try:
            db = DataBase()
            data = self.calendarWidget.selectedDate().toString('dd-MM-yyyy')
            doctor = db.login_auto_user()
            talons = [i for i in db.search(table="talons", word1="data", word2=data) if i[1] == doctor[1][0]]
            self.tableWidget.setRowCount(len(talons))
            self.tableWidget.setColumnCount(3)
            for i, elem in enumerate(talons):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(elem[0])))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(elem[2])))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(elem[3])))
        except IndexError:
            pass

    def addTalon(self):  # добавть талон
        self.label.hide()
        h, m = self.timeEdit.time().hour(), self.timeEdit.time().minute()
        data = self.calendarWidget.selectedDate().toString('dd-MM-yyyy')
        db = DataBase()
        result = db.new_talon(doctor=db.login_auto_user()[1][0], data=data, time=f"{h}:{m}")
        if not result:
            self.label.show()
        self.show_table()


class MyWidget8(MyWidget):  # открытие окна для выбора талона
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/talons_for_users.ui", self)
        self.comboBox.activated.connect(self.activ_1)
        self.comboBox_2.activated.connect(self.activ_2)
        self.calendarWidget.activated.connect(self.update_table)
        self.tableWidget.setDisabled(True)
        self.show_table()
        self.pushButton_2.clicked.connect(self.addTalon)
        self.pushButton_3.clicked.connect(self.back)
        self.talon = None
        self.label_4.hide()

    def back(self):
        ex2.show()
        ex2.updateTable()
        self.hide()

    def addTalon(self):  # взятие талона
        id_talon = str(self.lineEdit.text()).strip()
        if id_talon.isnumeric():
            db = DataBase()
            res = db.search("talons", "id", int(id_talon))
            if res and res[0][-1] == 0:
                id_talon_for_user = res[0][0]
                user = db.login_auto_user()
                db.update_db(table="talons", word1="user", word2=user[1][0], id_ud=id_talon_for_user)
                ex2.show()
                ex2.updateTable()
                self.hide()
            else:
                self.label_4.show()

    def update_table(self):
        self.show_table()

    def show_table(self):  # показ имеющихся талонов
        try:
            text = self.comboBox.currentText()
            text2 = self.comboBox_2.currentText()
            db = DataBase()
            data = self.calendarWidget.selectedDate().toString('dd-MM-yyyy')
            talons = db.search(table="talons", word1="data", word2=data)
            if text != "..." and text2 == "...":
                id_prof = db.search(table="professions", word1="name", word2=text, res="id")[0][0]
                doctors = [i[0] for i in db.search(table="doctors", word1="profession", word2=id_prof, res="id")]
                res = [db.search(table="talons", word1="doctor", word2=i) for i in doctors][0]
                talons = [i for i in res if i[2] == data]
            elif text != "..." and text2 != "...":
                id_prof = db.search(table="professions", word1="name", word2=text, res="id")[0][0]
                doctors = [i[0] for i in db.search(table="doctors", word1="profession", word2=id_prof, res="id")]
                res = [db.search(table="talons", word1="doctor", word2=i) for i in doctors]
                talons = [i for i in res[0] if i[2] == data]
            self.tableWidget.setRowCount(len(talons))
            self.tableWidget.setColumnCount(3)
            for i, elem in enumerate(talons):
                if elem[-1] == 0:
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(str(elem[0])))
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(db.search(table="doctors", word1="id",
                                                                              word2=int(elem[1]), res="name")[0][0]))
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(str(elem[3])))

        except IndexError:
            pass

    def activ_1(self):  # сортировка предложенных врачей по профессии и имени
        text = self.comboBox.currentText()
        if text != "...":
            self.comboBox_2.clear()
            db = DataBase()
            id_prof = db.search(table="professions", word1="name", word2=text)[0][0]
            self.comboBox_2.addItem("...")
            for i in db.search(table="doctors", word1="profession", word2=id_prof):
                self.comboBox_2.addItem(" ".join([str(i[0]), str(i[1])]))
        self.show_table()

    def activ_2(self):
        self.show_table()


class MyWidget9(MyWidget):  # открытие окна с информацией о пользователей
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/search.ui", self)
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.new_about)
        self.pushButton_3.clicked.connect(self.back)
        self.label.hide()
        self.true = False
        self.id = None

    def back(self):  # назад
        ex3.show()
        ex3.update_Table()
        self.hide()

    def search(self):  # открытие информации о пользователе
        self.label.hide()
        try:
            text = str(self.lineEdit.text()).strip()
            if text.isnumeric():
                db = DataBase()
                about = db.search(table="medical_cards", word1="id_medical_card", word2=int(text))
                self.id = about[0][0]
                about = about[0][-1]
                if about == "None" or about == "":
                    self.textEdit.setText("Пусто")
                else:
                    self.textEdit.setText(about)
            self.true = True
        except:
            self.label.show()
            self.true = False
            self.textEdit.setText("Ошибка")

    def new_about(self):  # обновление информации о пользователе
        text = str(self.textEdit.toPlainText())
        if self.true:
            db = DataBase()
            db.update_db(table="medical_cards", id_ud=self.id, word1="info_of_user", word2=text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = MyWidget()
    ex2 = MyWidget2()
    ex3 = MyWidget3()
    ex4 = MyWidget4()
    ex5 = MyWidget5()  # профиль doctor
    ex6 = MyWidget6()
    ex7 = MyWidget7()
    ex8 = MyWidget8()
    ex9 = MyWidget9()
    db_ = DataBase()
    data = db_.login_auto_user()

    if data and data[1]:
        if data[0] == "user":
            ex2.show()
        else:
            ex3.show()
    else:
        ex1.show()
    sys.exit(app.exec())
