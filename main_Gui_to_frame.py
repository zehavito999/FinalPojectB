# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap,QIcon
from user_Gui import user_Gui




import csv

class main_window_login(QWidget):
    def __init__(self, parent=None):
        super(main_window_login, self).__init__(parent)
        self.user_type_logged=""
        self.initUI()
        self.setFixedSize(1024,768)


    def initUI(self):
        """
        initialize UI objects
        """
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("Images/logo.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setWindowIcon(self.icon)

        self.main_login_frame=QtWidgets.QFrame(self)
        self.main_login_frame.setObjectName("MainLogin")
        self.main_login_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.main_login_frame)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1024, 768))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(220, 50, 521, 211))
        self.label.setPixmap(QtGui.QPixmap("Images/FINAL logo1.JPG"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.login_button=QtWidgets.QPushButton(self.frame)
        self.login_button.setGeometry(QtCore.QRect(430, 410, 261, 25))
        self.login_button.setStyleSheet("background-color: rgb(0, 170, 255);\n"
                                        "font: 25 14pt \"Calibri Light\";\n"
                                        "")
        self.login_button.setCheckable(False)
        self.login_button.setObjectName("login_button")
        self.username_label = QtWidgets.QLabel(self.frame)
        self.username_label.setGeometry(QtCore.QRect(310, 310, 101, 20))
        self.username_label.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.username_label.setScaledContents(True)
        self.username_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.username_label.setObjectName("username_label")
        self.password_label = QtWidgets.QLabel(self.frame)
        self.password_label.setGeometry(QtCore.QRect(310, 360, 111, 20))
        self.password_label.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.password_label.setScaledContents(True)
        self.password_label.setObjectName("password_label")
        self.username_line = QtWidgets.QLineEdit(self.frame)
        self.username_line.setGeometry(QtCore.QRect(430, 310, 261, 20))
        self.username_line.setStyleSheet("font: 25 10pt \"Calibri Light\";")
        self.username_line.setObjectName("username_line")
        self.password_line = QtWidgets.QLineEdit(self.frame)
        self.password_line.setGeometry(QtCore.QRect(430, 360, 261, 20))
        self.password_line.setStyleSheet("font: 25 10pt \"Calibri Light\";")
        self.password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line.setObjectName("password_line")
        self.lock_icon = QtWidgets.QLabel(self.frame)
        self.lock_icon.setGeometry(QtCore.QRect(990, 10, 21, 21))
        self.lock_icon.setPixmap(QtGui.QPixmap("Images/icons8-lock-26.png"))
        self.lock_icon.setScaledContents(True)
        self.lock_icon.setObjectName("lock_icon")
        self.current_logged_user = QtWidgets.QLabel(self.frame)
        self.current_logged_user.setGeometry(QtCore.QRect(840, 10, 141, 20))
        self.current_logged_user.setStyleSheet("font: 25 12pt \"Calibri Light\";")
        self.current_logged_user.setScaledContents(True)
        self.current_logged_user.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.current_logged_user.setObjectName("current_logged_user")
        self.retranslateUi1()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()


    def retranslateUi1(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainLogin", "Depression Detection Software"))
        self.login_button.setToolTip(_translate("MainLogin", "login button"))
        self.login_button.setText(_translate("MainLogin", "Login"))
        self.login_button.clicked.connect(self.login)  # Signal login function
        self.username_label.setText(_translate("MainLogin", "Username:"))
        self.password_label.setText(_translate("MainLogin", "Password:"))
        self.username_line.setToolTip(_translate("MainLogin", "enter username"))
        self.password_line.setToolTip(_translate("MainLogin", "enter password"))
        self.current_logged_user.setText(_translate("MainLogin", "Visitor"))


    def login(self):
        """
        login into the system, login details validation
        """
        flag=True
        if not self.username_line.text():
            self.username_line.setStyleSheet("border: 1.5px solid red;")
            flag=False
        else:
            self.username_line.setStyleSheet("border-color: 1px rgb(0, 0, 0);")
        if not self.password_line.text():
            self.password_line.setStyleSheet("border: 1.5px solid red;")
            flag = False
        else:
            self.password_line.setStyleSheet("border-color: 1px rgb(0, 0, 0);")
        if flag:
            type_user = self.search_users()
            self.user_type_logged=type_user
            if type_user:
                self.username_line.setText("")
                self.password_line.setText("")
                self.openUserGui()
            else:
                self.set_QMessageBox()


    def set_QMessageBox(self):
        """
        initialize QMessageBox
        """
        self.msg = QtWidgets.QMessageBox(self.main_login_frame)
        self.msg.setGeometry(QtCore.QRect(430, 310, 50, 20))
        self.msg.setIcon(QtWidgets.QMessageBox.Warning)
        self.msg.setText("User was not found")
        self.msg.setWindowTitle("Alert")
        self.msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
        self.msg.exec_()
        result=self.msg.clickedButton()
        if result.text()=="Retry":
            self.username_line.clear()
            self.password_line.clear()
            self.username_line.setStyleSheet("font: 25 10pt \"Calibri Light\";")
            self.password_line.setStyleSheet("font: 25 10pt \"Calibri Light\";")

    def search_users(self):
        """
        locating user on csv file
        :return:
        """
        self.current_user_list = []
        users_file=csv.DictReader(open("users.csv"))
        for row in users_file:
            username_file=row["username"]
            password_file=row["password"]
            type_file=row["type"]
            email_file=row["email"]
            if username_file==self.username_line.text() and password_file==self.password_line.text():
                self.current_user_list.append(username_file)
                self.current_user_list.append(password_file)
                self.current_user_list.append(type_file)
                self.current_user_list.append(email_file)
                return type_file
        return False

    def openUserGui(self):
        userGui=user_Gui(self)
        userGui.show()
        userGui.set_current_logged_user_label(self.current_user_list[0])
        self.frame.setVisible(False)
"""
    def openAdminGui(self):
        adminGui=admin_Gui(self)
        adminGui.show()
        adminGui.set_current_logged_user_label(self.current_user_list[0])
        self.frame.setVisible(False)
"""

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    main = main_window_login()
    sys.exit(app.exec_())
