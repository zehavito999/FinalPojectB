from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import QUrl, QDir, QTextStream, QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot
import twitter_services
import sys
import NeuralNetworkThread
from os import listdir
from os.path import isfile, join
from pandas import DataFrame
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import os
import statistics
from datetime import datetime
import csv
from Gui_services import gui_services


class user_Gui(QWidget):
    def __init__(self, parent=None):
        """
user UI constructor
        :param parent: inherent from main gui class
        """
        super(user_Gui, self).__init__(parent)
        self.gui_services=gui_services()
        self.operation_list = [] #documenting framing for back procedure
        self.model = NeuralNetworkThread.Neural_Network()
        self.model.load_model()  # loading the defult model
        self.initUI_user()
        self.setFixedSize(1024, 768) #setting the window to a fixed size
        self.user_type_logged = self.parent().user_type_logged
        if self.user_type_logged == "Admin":
            self.admin_raise()
        self.show()

    def initUI_user(self):
        """
initialize gui objects
        """
        self.user_main_gui = QtWidgets.QFrame(self)
        self.user_main_gui.setObjectName("UserGui")
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("Images/logo.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.user_main_gui.setWindowIcon(self.icon)
        self.user_main_gui.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame = QtWidgets.QFrame(self.user_main_gui)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1024, 768))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.vertical_frame = QtWidgets.QFrame(self.user_main_gui)
        self.vertical_frame.setGeometry(QtCore.QRect(0, -10, 241, 900))
        self.vertical_frame.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(123, 123, 123, 255), stop:1 rgba(255, 255, 255, 255));")
        self.vertical_frame.setObjectName("vertical_frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.vertical_frame)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_3.setContentsMargins(1, 1, 10, 600)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.run_analyze_button = QtWidgets.QPushButton(self.vertical_frame)
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(16)
        self.run_analyze_button.setFont(font)
        self.run_analyze_button.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.run_analyze_button.setObjectName("run_analyze_button")
        self.verticalLayout_3.addWidget(self.run_analyze_button.setGeometry(1, 50, 260, 30))
        self.results_button = QtWidgets.QPushButton(self.vertical_frame)
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(16)
        self.results_button.setFont(font)
        self.results_button.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.results_button.setObjectName("results_button")
        self.verticalLayout_3.addWidget(self.results_button.setGeometry(1, 100, 260, 30))
        # Admin features START
        self.model_settings_button = QtWidgets.QPushButton(self.vertical_frame)
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(16)
        self.model_settings_button.setFont(font)
        self.model_settings_button.setStyleSheet("background-color: rgb(0, 170, 255);\n" "")
        self.model_settings_button.setObjectName("model_settings_button")
        self.verticalLayout_3.addWidget(self.model_settings_button.setGeometry(1, 150, 260, 30))
        # Admin features END
        self.log_out_button = QtWidgets.QPushButton(self.vertical_frame)
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(16)
        self.log_out_button.setFont(font)
        self.log_out_button.setStyleSheet("")
        self.log_out_button.setObjectName("log_out_button")
        self.verticalLayout_3.addWidget(self.log_out_button.setGeometry(1, 720, 260, 30))
        self.logo_label = QtWidgets.QLabel(self.user_main_gui)
        self.logo_label.setGeometry(QtCore.QRect(390, 60, 391, 141))
        self.logo_label.setText("")
        self.logo_label.setPixmap(QtGui.QPixmap("Images/FINAL logo1.JPG"))
        self.logo_label.setScaledContents(True)
        self.logo_label.setObjectName("logo_label")
        self.about_frame = QtWidgets.QFrame(self.user_main_gui)
        self.about_frame.setGeometry(QtCore.QRect(200, 200, 781, 521))
        self.about_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.about_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.about_frame.setObjectName("about_frame")
        self.operation_list.append(self.about_frame)
        self.about_textEdit = QtWidgets.QTextEdit(self.about_frame)
        self.about_textEdit.setGeometry(QtCore.QRect(230, 30, 361, 271))
        self.about_textEdit.setStyleSheet("font: 25 12pt \"Calibri Light\";")
        self.about_textEdit.setObjectName("about_textEdit")
        self.unlock_label = QtWidgets.QLabel(self.user_main_gui)
        self.unlock_label.setGeometry(QtCore.QRect(990, 10, 21, 20))
        self.unlock_label.setText("")
        self.unlock_label.setPixmap(QtGui.QPixmap("Images/icons8-padlock-26.png"))
        self.unlock_label.setScaledContents(True)
        self.unlock_label.setObjectName("unlock_label")
        self.current_logged_user_label = QtWidgets.QLabel(self.user_main_gui)
        self.current_logged_user_label.setGeometry(QtCore.QRect(770, 10, 211, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(12)
        self.current_logged_user_label.setFont(font)
        self.current_logged_user_label.setText("")
        self.current_logged_user_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.current_logged_user_label.setObjectName("current_logged_user_label")
        self.back_button = QtWidgets.QPushButton(self.frame)
        self.back_button.setGeometry(QtCore.QRect(970, 720, 41, 41))
        self.back_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Images/return.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back_button.setIcon(icon1)
        self.back_button.setIconSize(QtCore.QSize(25, 25))
        self.back_button.setObjectName("back_button")
        self.back_button.setVisible(False)
        self.home_button = QtWidgets.QPushButton(self.frame)
        self.home_button.setGeometry(QtCore.QRect(250, 10, 41, 41))
        self.home_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Images/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.home_button.setIcon(icon2)
        self.home_button.setIconSize(QtCore.QSize(25, 25))
        self.home_button.setObjectName("home_button")
        self.vertical_frame.raise_()
        self.logo_label.raise_()
        self.about_textEdit.raise_()
        self.unlock_label.raise_()
        self.current_logged_user_label.raise_()
        self.retranslateUi2()
        # self.train_and_validate_button.setVisible(False)
        self.model_settings_button.setVisible(False)
        QtCore.QMetaObject.connectSlotsByName(self.user_main_gui)

    def retranslateUi2(self):
        """
        initialize gui objects text
        """
        self._translate = QtCore.QCoreApplication.translate
        self.user_main_gui.setWindowTitle(self._translate("UserGui", "Depression Detection Software"))
        self.run_analyze_button.setToolTip(self._translate("UserGui", "Run new analyze"))
        self.run_analyze_button.setText(self._translate("UserGui", "Run Analyze"))
        self.run_analyze_button.clicked.connect(self.run_analyze)
        self.results_button.setToolTip(self._translate("UserGui", "Analyze results"))
        self.results_button.setText(self._translate("UserGui", "Analyze Results"))
        self.results_button.clicked.connect(self.init_results)
        self.model_settings_button.setToolTip(self._translate("UserGui", "Neural network model settings"))
        self.model_settings_button.setText(self._translate("UserGui", "Model Settings"))
        self.model_settings_button.clicked.connect(self.model_settings_func)  # signal model setting function
        self.log_out_button.setToolTip(self._translate("UserGui", "Log out "))
        self.log_out_button.setText(self._translate("UserGui", "Log out"))
        self.log_out_button.clicked.connect(self.logout)
        self.about_textEdit.setHtml(self._translate("UserGui",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'Calibri Light\'; font-size:12pt; font-weight:200; font-style:normal;\">\n"
                                                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">This application was developed by Dvir Kovalio and Zehavit Otmazgin.</span></p>\n"
                                                    "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">On this application you will be able to detect wheter a user is depressed or control according to his Tweets.</span></p></body></html>"))
        self.back_button.setToolTip(self._translate("UserGui", "Return"))
        self.back_button.clicked.connect(self.back_func)
        self.home_button.setToolTip(self._translate("UserGui", "Home"))
        self.home_button.clicked.connect(self.go_home)

    def set_current_logged_user_label(self, user_log_in):
        """
        set current logged user label while logging in
        :param x: username string
        """
        self.username_label = user_log_in
        self.current_logged_user_label.setText(self._translate("UserGui", user_log_in))

    def admin_raise(self):
        """
        adding administrator only button
        """
        self.model_settings_button.setVisible(True)

    def go_home(self):
        """
        display main screen while clicking 'home' button icon
        """
        self.operation_list[-1].hide()
        self.operation_list[0].show()
        self.back_button.setVisible(False)
        last_screen = self.operation_list[0]
        self.operation_list = [last_screen]

    def back_func(self):
        """
        display previous frame
        """
        if len(self.operation_list) > 1:
            left_frame = self.operation_list.pop()
            left_frame.hide()
            self.operation_list[-1].show()
        else:
            self.go_home()

    def init_results(self):
        """
        initizalize results page, adding to operation_list for 'back' button
        """
        self.operation_list[-1].hide()
        self.display_analyze_results() #building analyze results table frame
        if not self.operation_list[-1].objectName() == "analyze_results_frame":
            self.operation_list.append(self.analyze_results_frame)

    def display_analyze_results(self):#TODO:SPLIT?
        """
        create frame and display analyze results table
        """
        self.analyze_results_frame = QtWidgets.QFrame(self.frame)
        self.analyze_results_frame.setGeometry(QtCore.QRect(200, 200, 781, 521))
        self.analyze_results_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.analyze_results_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.analyze_results_frame.setObjectName("analyze_results_frame")
        self.analyze_results_frame.setVisible(True)
        with open("analyze_results.csv", "r") as f:
            one_char=f.read(1)
            if not one_char:#if file is empty
                self.no_res_label = QtWidgets.QLabel(self.analyze_results_frame)
                self.no_res_label.setStyleSheet("font: 25 18pt \"Calibri Light\";")
                self.no_res_label.setGeometry(QtCore.QRect(320, 10, 250, 40))
                self.no_res_label.setText("No available results")
                self.no_res_label.setVisible(True)
                return
            else:
                self.reader = csv.reader(f, delimiter=",")
                data = list(self.reader)
                self.row_count = len(data)
        self.yes_res_label = QtWidgets.QLabel(self.analyze_results_frame)
        self.yes_res_label.setStyleSheet("font: 25 18pt \"Calibri Light\";")
        self.yes_res_label.setGeometry(QtCore.QRect(320, 10, 250, 30))
        self.yes_res_label.setText("Analyze results")
        self.yes_res_label.setVisible(True)
        self.frame_for_table = QtWidgets.QFrame(self.analyze_results_frame)
        self.frame_for_table.setGeometry(QtCore.QRect(90, 50, 635, 450))
        self.frame_for_table.setVisible(True)
        self.table = QTableWidget(self.frame_for_table)
        self.table.setRowCount(self.row_count)
        self.table.setColumnCount(6)
        labels = ["Time", "Twitter username", "Tweets amount", "Depression severity", "Model name", "Graph"]
        self.table.setHorizontalHeaderLabels(labels)
        self.layoutVertical = QtWidgets.QVBoxLayout(self.frame_for_table)
        self.layoutVertical.addWidget(self.table)
        self.btns_objs = [QtWidgets.QPushButton(self.frame_for_table) for k in range(self.row_count)]
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Images/graph.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.row_count_temp = 0
        self.row_count_plus_one = self.row_count + 1
        self.list_of_x_y_lists = []
        self.twitter_user_lst = []
        with open("analyze_results.csv", "r") as fileInput:
            included_cols = [0, 1, 2, 3, 4]
            for row in csv.reader(fileInput):
                if self.row_count_temp != self.row_count_plus_one:
                    content = list(row[i] for i in included_cols)
                    self.table.setItem(self.row_count_temp, 0, QtGui.QTableWidgetItem(content[0]))
                    self.table.setItem(self.row_count_temp, 1, QtGui.QTableWidgetItem(content[1]))
                    self.table.setItem(self.row_count_temp, 2, QtGui.QTableWidgetItem(content[2]))
                    self.table.setItem(self.row_count_temp, 3, QtGui.QTableWidgetItem(content[3]))
                    self.table.setItem(self.row_count_temp, 4, QtGui.QTableWidgetItem(content[4]))
                    self.btns_objs[self.row_count_temp].setIcon(icon1)
                    self.btns_objs[self.row_count_temp].setIconSize(QtCore.QSize(25, 25))
                    self.twitter_user=row[1]
                    self.twitter_user_lst.append(self.twitter_user[:])
                    self.x_res = row[5]
                    self.y_res = row[6]
                    self.list_of_x_y_lists.append((self.x_res[:], self.y_res[:]))
                    self.btns_objs[self.row_count_temp].clicked.connect(self.set_graph_to_table)
                    self.btns_objs[self.row_count_temp].setText(str(self.row_count_temp))
                    self.btns_objs[self.row_count_temp].setStyleSheet("color: white")
                    self.table.setCellWidget(self.row_count_temp, 5, self.btns_objs[self.row_count_temp])
                    self.row_count_temp = self.row_count_temp + 1

    def set_graph_to_table(self):
        """
        handeling with specific button according to user's choice and plotting graph according to saving (x;y)'s
        """
        x = self.focusWidget()
        x_num = int(x.text())
        tmp_lst = self.list_of_x_y_lists[x_num]
        twt_lst=self.twitter_user_lst[x_num]
        self.gui_services.plot(tmp_lst,twt_lst)

    def run_analyze(self):
        """
        calling to building run analyze frame function
        """
        self.operation_list[-1].hide()
        self.init_analyze()
        if not self.operation_list[-1].objectName() == "scene_run_analyze_frame":
            self.operation_list.append(self.scene_run_analyze_frame)

    def init_analyze(self):
        """
        building run analyze frame
        """
        self.scene_run_analyze_frame = QtWidgets.QFrame(self.frame)
        self.scene_run_analyze_frame.setGeometry(QtCore.QRect(200, 200, 781, 521))
        self.scene_run_analyze_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.scene_run_analyze_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.scene_run_analyze_frame.setObjectName("scene_run_analyze_frame")
        self.tested_name_label = QtWidgets.QLabel(self.scene_run_analyze_frame)
        self.tested_name_label.setGeometry(QtCore.QRect(180, 30, 140, 16))
        self.tested_name_label.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.tested_name_label.setObjectName("tested_name_label")
        self.tested_name_line_edit = QtWidgets.QLineEdit(self.scene_run_analyze_frame)
        self.tested_name_line_edit.setGeometry(QtCore.QRect(340, 30, 241, 20))
        self.tested_name_line_edit.setObjectName("tested_name_line_edit")
        self.tested_name_line_edit.setStyleSheet("font: 25 12pt \"Calibri Light\";")
        self.tested_id_count_label = QtWidgets.QLabel(self.scene_run_analyze_frame)
        self.tested_id_count_label.setGeometry(QtCore.QRect(180, 70, 140, 16))
        self.tested_id_count_label.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.tested_id_count_label.setObjectName("tested_id_count_label")
        self.tested_id_count_line_edit = QtWidgets.QLineEdit(self.scene_run_analyze_frame)
        self.tested_id_count_line_edit.setGeometry(QtCore.QRect(340, 70, 241, 20))
        self.tested_id_count_line_edit.setStyleSheet("font: 25 12pt \"Calibri Light\";")
        self.tested_id_count_line_edit.setObjectName("tested_id_count_line_edit")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Images/upload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.extract_tweets_button = QtWidgets.QPushButton(self.scene_run_analyze_frame)
        self.extract_tweets_button.setGeometry(QtCore.QRect(340, 110, 241, 20))
        self.extract_tweets_button.setStyleSheet(
            "font: 25 14pt \"Calibri Light\";\n" "background-color: rgb(0, 170, 255);")
        self.extract_tweets_button.setObjectName("extract_tweets_button")
        self.extract_tweets_button.clicked.connect(self.extract_tweets)
        self._translate = QtCore.QCoreApplication.translate
        self.tested_name_label.setText(self._translate("UserGui", "Twitter Username:"))
        self.tested_name_line_edit.setToolTip(self._translate("UserGui", "Enter twitter username"))
        self.tested_id_count_label.setText(self._translate("UserGui", "Tweets Amount:"))
        self.tested_id_count_line_edit.setToolTip(self._translate("UserGui", "Enter amount of tweets"))
        self.extract_tweets_button.setToolTip(self._translate("UserGui", "Click to extract tweets"))
        self.extract_tweets_button.setText(self._translate("UserGui", "Extract Tweets"))
        self.back_button.setVisible(True)
        self.scene_run_analyze_frame.setVisible(True)

    def set_gif(self):
        """
        creating blue spinner run analyze gif
        """
        self.label_load_gif = QtWidgets.QLabel(self.scene_run_analyze_frame)
        self.label_load_gif.setGeometry(600, 95, 50, 50)
        self.animation_load = QMovie("Images/loading_gif.gif")
        self.label_load_gif.setMovie(self.animation_load)
        self.animation_load.start()
        self.label_load_gif.setVisible(True)

    def model_settings_func(self):
        """
        calling to building model settings frame function
        """
        self.operation_list[-1].hide()
        self.model_path_directory = QDir("models")
        self.init_model_settings()
        self.select_model_comboBox_setting_given.currentIndexChanged.connect(self.update_existed_model_fields)
        if not self.operation_list[-1].objectName() == "scene_model_settings":
            self.operation_list.append(self.scene_model_settings)

    def init_model_settings(self):
        """
        building model settings frame
        """
        self.scene_model_settings = QtWidgets.QFrame(self.frame)
        self.scene_model_settings.setGeometry(QtCore.QRect(200, 200, 781, 521))
        self.scene_model_settings.setStyleSheet("gridline-color: rgb(0, 255, 0);")
        self.scene_model_settings.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.scene_model_settings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.scene_model_settings.setObjectName("scene_model_settings")
        self.divider_label = QtWidgets.QLabel(self.scene_model_settings)
        self.divider_label.setGeometry(QtCore.QRect(410, 30, 16, 201))
        self.divider_label.setPixmap(QtGui.QPixmap("Images/straight_line.PNG"))
        self.select_model_label_setting_given = QtWidgets.QLabel(self.scene_model_settings)
        self.select_model_label_setting_given.setGeometry(QtCore.QRect(450, 25, 114, 33))
        self.select_model_label_setting_given.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.select_model_label_setting_given.setObjectName("select_model_label_setting_given")
        self.select_model_comboBox_setting_given = QtWidgets.QComboBox(self.scene_model_settings)
        self.select_model_comboBox_setting_given.setGeometry(QtCore.QRect(620, 30, 111, 22))
        self.select_model_comboBox_setting_given.setStyleSheet("font: 25 12pt \"Calibri Light\";")
        self.select_model_comboBox_setting_given.setObjectName("select_model_comboBox_setting_given")
        self.models_folder_list = self.gui_services.extract_files_to_list()
        for model in self.models_folder_list:
            self.select_model_comboBox_setting_given.addItem(model)
        self.batch_size_label_given = QtWidgets.QLabel(self.scene_model_settings)
        self.batch_size_label_given.setGeometry(QtCore.QRect(450, 70, 114, 33))
        self.batch_size_label_given.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.batch_size_label_given.setObjectName("batch_size_label_given")
        self.epoch_number_label_given = QtWidgets.QLabel(self.scene_model_settings)
        self.epoch_number_label_given.setGeometry(QtCore.QRect(450, 110, 114, 33))
        self.epoch_number_label_given.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.epoch_number_label_given.setObjectName("epoch_number_label_given")
        self.filter_number_label_given = QtWidgets.QLabel(self.scene_model_settings)
        self.filter_number_label_given.setGeometry(QtCore.QRect(450, 150, 131, 33))
        self.filter_number_label_given.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.filter_number_label_given.setObjectName("filter_number_label_given")
        self.optimizer_label_given = QtWidgets.QLabel(self.scene_model_settings)
        self.optimizer_label_given.setGeometry(QtCore.QRect(450, 190, 114, 33))
        self.optimizer_label_given.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.optimizer_label_given.setObjectName("optimizer_label_given")
        self.batch_size_line_given = QtWidgets.QLineEdit(self.scene_model_settings)
        self.batch_size_line_given.setGeometry(QtCore.QRect(620, 75, 111, 20))
        self.batch_size_line_given.setStyleSheet("font: 25 12pt \"Calibri Light\";")
        self.batch_size_line_given.setObjectName("batch_size_line_given")
        self.batch_size_line_given.setText(str(self.model.batch_size))
        self.batch_size_line_given.setEnabled(False)
        self.epoch_number_line_given = QtWidgets.QLineEdit(self.scene_model_settings)
        self.epoch_number_line_given.setGeometry(QtCore.QRect(620, 115, 111, 20))
        self.epoch_number_line_given.setStyleSheet("font: 12pt \"Calibri\";")
        self.epoch_number_line_given.setObjectName("epoch_number_line_given")
        self.epoch_number_line_given.setText(str(self.model.epochs))
        self.epoch_number_line_given.setEnabled(False)
        self.filter_number_line_given = QtWidgets.QLineEdit(self.scene_model_settings)
        self.filter_number_line_given.setGeometry(QtCore.QRect(620, 155, 111, 20))
        self.filter_number_line_given.setStyleSheet("font: 25 12pt \"Calibri Light\";")
        self.filter_number_line_given.setObjectName("filter_number_line_given")
        self.filter_number_line_given.setText(str(self.model.filters))
        self.filter_number_line_given.setEnabled(False)
        self.optimizer_comboBox_given = QtWidgets.QLineEdit(self.scene_model_settings)
        self.optimizer_comboBox_given.setGeometry(QtCore.QRect(620, 190, 111, 22))
        self.optimizer_comboBox_given.setStyleSheet("font: 25 12pt \"Calibri Light\";")
        self.optimizer_comboBox_given.setObjectName("optimizer_comboBox_given")
        self.optimizer_comboBox_given.setText(str(self.model.optimizer))
        self.optimizer_comboBox_given.setEnabled(False)
        self.start_button = QtWidgets.QPushButton(self.scene_model_settings)
        self.start_button.setGeometry(QtCore.QRect(90, 250, 275, 20))
        self.start_button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.start_button.setToolTipDuration(-1)
        self.start_button.setStyleSheet("background-color: rgb(0, 170, 255);\n"
                                        "font: 25 14pt \"Calibri Light\";\n"
                                        "")
        self.start_button.setCheckable(False)
        self.start_button.setAutoRepeat(False)
        self.start_button.setObjectName("start_button")
        self.start_button.clicked.connect(self.validate_model_settings)
        self._translate = QtCore.QCoreApplication.translate
        self.select_model_label_setting_given.setText(self._translate("UserGui", "Select Model:"))
        self.batch_size_label_given.setText(self._translate("UserGui", "Batch Size:"))
        self.epoch_number_label_given.setText(self._translate("UserGui", "Epoch Number:"))
        self.filter_number_label_given.setText(self._translate("UserGui", "Filter Number:"))
        self.optimizer_label_given.setText(self._translate("UserGui", "Optimizer:"))
        self.batch_size_line_given.setToolTip(self._translate("UserGui", "current model batch size"))
        self.epoch_number_line_given.setToolTip(self._translate("UserGui", "current model epoch number"))
        self.filter_number_line_given.setToolTip(self._translate("UserGui", "current model filter number"))
        self.optimizer_comboBox_given.setToolTip(self._translate("UserGui", "current model optimizer"))
        self.select_model_comboBox_setting_given.setToolTip(self._translate("UserGui", "choose model"))
        self.start_button.setToolTip(self._translate("UserGui", "start create new model process"))
        self.start_button.setText(self._translate("UserGui", "Create New Model"))
        self.batch_size_label = QtWidgets.QLabel(self.scene_model_settings)
        self.batch_size_label.setGeometry(QtCore.QRect(90, 70, 114, 33))
        self.batch_size_label.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.batch_size_label.setObjectName("batch_size_label")
        self.epoch_number_label = QtWidgets.QLabel(self.scene_model_settings)
        self.epoch_number_label.setGeometry(QtCore.QRect(90, 110, 131, 33))
        self.epoch_number_label.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.epoch_number_label.setObjectName("epoch_number_label_given")
        self.filter_number_label = QtWidgets.QLabel(self.scene_model_settings)
        self.filter_number_label.setGeometry(QtCore.QRect(90, 150, 131, 33))
        self.filter_number_label.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.filter_number_label.setObjectName("filter_number_label")
        self.optimizer_label = QtWidgets.QLabel(self.scene_model_settings)
        self.optimizer_label.setGeometry(QtCore.QRect(90, 190, 114, 20))
        self.optimizer_label.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.optimizer_label.setObjectName("optimizer_label")
        self.batch_size_line = QtWidgets.QLineEdit(self.scene_model_settings)
        self.batch_size_line.setGeometry(QtCore.QRect(260, 75, 111, 20))
        self.batch_size_line.setStyleSheet("font: 25 12pt \"Calibri Light\";")
        self.batch_size_line.setObjectName("batch_size_line")
        self.epoch_number_line = QtWidgets.QLineEdit(self.scene_model_settings)
        self.epoch_number_line.setGeometry(QtCore.QRect(260, 115, 111, 20))
        self.epoch_number_line.setStyleSheet("font: 12pt \"Calibri\";")
        self.epoch_number_line.setObjectName("epoch_number_line")
        self.filter_number_line = QtWidgets.QLineEdit(self.scene_model_settings)
        self.filter_number_line.setGeometry(QtCore.QRect(260, 155, 111, 20))
        self.filter_number_line.setStyleSheet("font: 25 12pt \"Calibri Light\";")
        self.filter_number_line.setObjectName("filter_number_line")
        self.optimizer_comboBox = QtWidgets.QComboBox(self.scene_model_settings)
        self.optimizer_comboBox.setGeometry(QtCore.QRect(260, 190, 111, 22))
        self.optimizer_comboBox.setStyleSheet("font: 25 12pt \"Calibri Light\";")
        self.optimizer_comboBox.setObjectName("optimizer_comboBox")
        self.init_cbx()
        self.batch_size_label.setText(self._translate("UserGui", "Batch Size:"))
        self.epoch_number_label.setText(self._translate("UserGui", "Epoch Number:"))
        self.filter_number_label.setText(self._translate("UserGui", "Filter Number:"))
        self.batch_size_line.setToolTip(self._translate("UserGui", "enter batch size"))
        self.epoch_number_line.setToolTip(self._translate("UserGui", "enter epoch number"))
        self.filter_number_line.setToolTip(self._translate("UserGui", "enter filter number"))
        self.optimizer_comboBox.setToolTip(self._translate("UserGui", "choose optimizer"))
        self.optimizer_label.setText(self._translate("UserGui", "Optimizer:"))
        # self.select_model_comboBox_setting_given.activated[str].connect(self.update_existed_model_fields)
        self.scene_model_settings.setVisible(True)

    def update_existed_model_fields(self):
        """
        updating hyperparameters of existed models
        """
        self.model.load_model(self.select_model_comboBox_setting_given.currentText())
        self.batch_size_line_given.setText(str(self.model.batch_size))
        self.epoch_number_line_given.setText(str(self.model.epochs))
        self.filter_number_line_given.setText(str(self.model.filters))
        self.optimizer_comboBox_given.setText(str(self.model.optimizer))

    def init_cbx(self):
        """
        initialize optimizer combobox with 3 optimizers name
        """
        self.optimizer_list = ['nadam', 'sgd', 'rmsprop']
        for optimizer in self.optimizer_list:
            self.optimizer_comboBox.addItem(optimizer)

    def extract_tweets(self):
        """
        validating parameters and then extracting tweets by using tweepy API
        """
        flag = True
        if not self.tested_name_line_edit.text():
            self.tested_name_line_edit.setStyleSheet("border: 1.5px solid red;")
            flag = False
        else:
            self.tested_name_line_edit.setStyleSheet("border-color: 1px rgb(0, 0, 0);")
        if not self.tested_id_count_line_edit.text():
            self.tested_id_count_line_edit.setStyleSheet("border: 1.5px solid red;")
            flag = False
        else:
            self.tested_id_count_line_edit.setStyleSheet("border-color: 1px rgb(0, 0, 0);")
        if flag:
            self.count_to_int = int(self.tested_id_count_line_edit.text())
            self.twitter_extraction_thread = twitter_services.twitter_api(self.tested_name_line_edit.text(),
                                                                          self.count_to_int)
            self.twitter_extraction_thread.taskFinished.connect(self.twitter_extraction_thread_on_finish)
            self.twitter_extraction_thread_start()

    @QtCore.pyqtSlot()
    def twitter_extraction_thread_on_finish(self):
        """
        thread operation- export data from twitter by using tweepy API
        """
        self.label_load_gif.setVisible(False)
        try:
            if not len(self.twitter_extraction_thread.all_tweets_list):
                self.set_QMessageBox_Retry("Twitter user don't have available tweets!")
            else:
                self.display_tweets()
        except AttributeError:
            self.set_QMessageBox_Retry_user_not_exists()

    def twitter_extraction_thread_start(self):
        self.set_gif()
        self.twitter_extraction_thread.start()

    def display_tweets(self):
        """
        initialize display tweets on run analyze page
        """
        self.tweets_list_input = []
        self.display_tweets_frame = QtWidgets.QFrame(self.frame)
        self.display_tweets_frame.setGeometry(QtCore.QRect(200, 200, 781, 521))
        self.display_tweets_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.display_tweets_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.display_tweets_frame.setObjectName("display_tweets_frame")
        self.tweets_plainTextEdit = QtWidgets.QPlainTextEdit(self.display_tweets_frame)
        self.tweets_plainTextEdit.setGeometry(QtCore.QRect(210, 60, 380, 200))
        self.select_model_label = QtWidgets.QLabel(self.display_tweets_frame)
        self.select_model_label.setGeometry(QtCore.QRect(210, 280, 114, 33))
        self.select_model_label.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.select_model_label.setObjectName("select_model_label")
        self.select_model_comboBox = QtWidgets.QComboBox(self.display_tweets_frame)
        self.select_model_comboBox.setGeometry(QtCore.QRect(330, 285, 261, 20))
        self.select_model_comboBox.setStyleSheet("font: 25 12pt \"Calibri Light\";")
        self.select_model_comboBox.setObjectName("select_model_comboBox")
        self.models_folder_list = self.gui_services.extract_files_to_list()
        for file in self.models_folder_list:
            self.select_model_comboBox.addItem(file)
        self.start_run_button = QtWidgets.QPushButton(self.display_tweets_frame)
        self.start_run_button.setGeometry(QtCore.QRect(210, 400, 380, 20))
        self.start_run_button.setStyleSheet("font: 25 14pt \"Calibri Light\";\n" "background-color: rgb(0, 170, 255);")
        self.start_run_button.setObjectName("start_run_button")
        self.start_run_button.clicked.connect(self.start_run)
        self.start_run_button.setToolTip(self._translate("UserGui", "Click to start analyze"))
        self.start_run_button.setText(self._translate("UserGui", "Run Analyze"))
        self.select_model_label.setText(self._translate("UserGui", "Select Model:"))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(12)
        self.tweets_plainTextEdit.setFont(font)
        self.tweets_plainTextEdit.setObjectName("tweets_plainTextEdit")
        self.tweets_plainTextEdit.verticalScrollBar().minimum()
        if len(self.twitter_extraction_thread.all_tweets_list) > self.count_to_int:
            temp = len(self.twitter_extraction_thread.all_tweets_list) - self.count_to_int
            self.twitter_extraction_thread.all_tweets_list = self.twitter_extraction_thread.all_tweets_list[: -temp]
        for tweet in self.twitter_extraction_thread.tweets[:self.count_to_int]:
            self.tweets_plainTextEdit.appendPlainText(str(tweet._json['id']) + " " + tweet._json['full_text'] + '\n')
            self.tweets_list_input.append([tweet._json['full_text']])  # input to neural network
        self.scene_run_analyze_frame.setVisible(False)
        self.display_tweets_frame.setVisible(True)
        if len(self.twitter_extraction_thread.all_tweets_list) != self.count_to_int:
            temp = len(self.twitter_extraction_thread.all_tweets_list)
            self.set_QMessageBox_Ok("Only {} out of {} tweets were extracted".format(temp, self.count_to_int))

    @QtCore.pyqtSlot()
    def predict_therad_thread_finish(self):
        self.init_classification_frame()

    def start_run(self):
        """
        Activating classification process on a QThread class
        """
        self.predict_therad = NeuralNetworkThread.Neural_Network.predict("default", self.tweets_list_input)
        self.predict_therad.taskFinished.connect(self.predict_therad_thread_finish)
        self.predict_therad.start()

    def set_QMessageBox_Retry(self, error_str):
        """
        run analyze QMessageBox: if user don't have tweets
        :param error_str: printing message
        """
        self.msg = QtWidgets.QMessageBox(self.scene_run_analyze_frame)
        self.msg.setGeometry(QtCore.QRect(430, 310, 50, 20))
        self.msg.setWindowIcon(QtGui.QIcon("Images/logo.PNG"))
        self.msg.setIcon(QtWidgets.QMessageBox.Warning)
        self.msg.setText(error_str)
        self.msg.setWindowTitle("Information")
        self.msg.setStandardButtons(QMessageBox.Retry)
        self.msg.exec_()
        result = self.msg.clickedButton()
        if result.text() == "Retry":
            self.tested_name_line_edit.clear()
            self.tested_id_count_line_edit.clear()

    def set_QMessageBox_Retry_user_not_exists(self):
        """
        run analyze twitter user do not exists
        """
        self.msg = QtWidgets.QMessageBox(self.scene_run_analyze_frame)
        self.msg.setGeometry(QtCore.QRect(430, 310, 50, 20))
        self.msg.setWindowIcon(QtGui.QIcon("Images/logo.PNG"))
        self.msg.setIcon(QtWidgets.QMessageBox.Warning)
        self.msg.setText("User not exists!")
        self.msg.setWindowTitle("Error")
        self.msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
        self.msg.exec_()
        result = self.msg.clickedButton()
        if result.text() == "Retry":
            self.tested_name_line_edit.clear()
            self.tested_id_count_line_edit.clear()

    def set_QMessageBox_Ok(self, ok_str):
        """
        run analyze semi-extraction of tweets
        :param ok_str: number of tweets out of X that were extracted
        """
        self.msg = QtWidgets.QMessageBox(self.scene_run_analyze_frame)
        self.msg.setGeometry(QtCore.QRect(430, 310, 50, 20))
        self.msg.setWindowIcon(QtGui.QIcon("Images/logo.PNG"))
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setText(ok_str)
        self.msg.setWindowTitle("Information")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()

    def init_classification_frame(self):
        """
        building classification result frame
        """
        self.display_tweets_frame.setVisible(False)
        self.classification_scene = QtWidgets.QFrame(self.frame)
        self.classification_scene.setGeometry(QtCore.QRect(200, 200, 781, 521))
        self.classification_scene.setStyleSheet("gridline-color: rgb(0, 255, 0);")
        self.classification_scene.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.classification_scene.setFrameShadow(QtWidgets.QFrame.Raised)
        self.classification_scene.setObjectName("classification_scene")
        self.classification_scene.setVisible(True)
        self.plot_frame = QtWidgets.QFrame(self.classification_scene)
        self.plot_frame.setGeometry(QtCore.QRect(200, 30, 400, 350))
        self.plot_frame.setStyleSheet("gridline-color: rgb(0, 255, 0);")
        self.plot_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plot_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plot_frame.setObjectName("plot_frame")
        self.plot_frame.setVisible(True)
        self.plot_widget_layout = QtWidgets.QGridLayout(self.plot_frame)
        self.plot_widget_layout.setGeometry(QtCore.QRect(105, 30, 350, 350))
        self.plot_widget_layout.setObjectName("plot_widget_layout")
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        self.graphWidget.setTitle("Depression severity per tweet:\n {}".format(self.tested_name_line_edit.text()))
        self.graphWidget.setLabel('left', 'Depression Severity')
        self.graphWidget.setLabel('bottom', 'Tweets')
        self.graphWidget.plotItem.getAxis('left').setPen(pg.mkPen(color=(0, 0, 0), width=1))
        self.graphWidget.plotItem.getAxis('bottom').setPen(pg.mkPen(color=(0, 0, 0), width=1))
        self.plot_widget_layout.addWidget(self.graphWidget, 2, 1)
        self.temp = list(range(0, len(self.predict_therad.result)))
        self.flat_list = [item for sublist in self.predict_therad.result for item in sublist]
        self.graphWidget.plot(self.temp, self.flat_list, pen=pg.mkPen(color=(0, 0, 0), width=2))
        self.graphWidget.setEnabled(True)
        self.avg = sum(self.flat_list) / len(self.flat_list)
        self.avg = self.avg.round(decimals=2)
        self.avg=self.avg*100
        self.avg_label = QtWidgets.QLabel(self.classification_scene)
        self.avg_label.setGeometry(QtCore.QRect(310, 400, 350, 20))
        self.avg_label.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.avg_label.setText("Depression severity is: {:.2f}%".format(self.avg))
        self.avg_label.setVisible(True)
        self.dict_analyze_results = {"timestamp": datetime.now(), "twitter_username": self.tested_name_line_edit.text(),
                                     "tweets_amount": len(self.predict_therad.result),
                                     "avg": str(self.avg), "model_name": self.select_model_comboBox.currentText(),
                                     "graph_x": self.temp, "graph_y": self.flat_list}
        self.gui_services.append_dict_as_row(self.dict_analyze_results)

    def start_model_settings(self):
        """
        start execute model settings
        """
        self.init_build_model_frame()
        self.model_therad = NeuralNetworkThread.Neural_Network.buildNeuralNetwork(self.graphWidget_build_model,
                                                                                  self.log_plainTextEdit,
                                                                                  self.optimizer_comboBox.currentText(),
                                                                                  self.filter_number_line.text(),
                                                                                  self.batch_size_line.text(),
                                                                                  self.epoch_number_line.text())
        self.model_therad.taskFinished.connect(self.model_therad_finish)
        self.model_therad.start()

    def model_therad_finish(self):
        self.build_label.setText("Finished!")
        self.label_load_gif.setVisible(False)
        self.msg = QtWidgets.QMessageBox(self.scene_model_settings)
        self.msg.setGeometry(QtCore.QRect(430, 310, 50, 20))
        self.msg.setWindowIcon(QtGui.QIcon("Images/logo.PNG"))
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setText(
            "The acc is: {:.4f} the loss is: {:.4f}.\nIf you would like to save only the model- click 'Save'\nIf you would like to save model and model summary file- click 'Save All'\nIf you do not want to save nothing- click 'Discard'".format(
                self.model_therad.outter.hist.history['acc'][-1],
                self.model_therad.outter.hist.history['val_loss'][-1]))
        self.msg.setWindowTitle("Information")
        self.msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.SaveAll)
        self.msg.exec_()
        result = self.msg.clickedButton()
        if result.text() == "Save":  # if user wants to save the model, he can insert model name to line edit and also download model.hist .txt file
            self.save_only_model()
        if result.text() == "Save All":
            self.save_model_and_hist()
        if result.text() == "Discard":  # if user dont want to save model, go back to main screen
            self.go_home()

    def save_only_model(self):
        """
        creating saving model's option objects
        """
        self.build_label.setVisible(False)
        self.save_model_label = QtWidgets.QLabel(self.build_model_scene)
        self.save_model_label.setGeometry(QtCore.QRect(90, 300, 300, 20))
        self.save_model_label.setStyleSheet("font: 25 12pt \"Calibri Light\";")
        self.save_model_label.setObjectName("save_model_label")
        self.save_model_label.setText("Insert model name:")
        self.save_model_label.setVisible(True)
        self.save_model_lineEdit = QtWidgets.QLineEdit(self.build_model_scene)
        self.save_model_lineEdit.setGeometry(QtCore.QRect(90, 340, 300, 20))
        self.save_model_lineEdit.setObjectName("save_model_lineEdit")
        self.save_model_lineEdit.setVisible(True)
        self.save_model_button = QtWidgets.QPushButton(self.build_model_scene)
        self.save_model_button.setStyleSheet("font: 25 14pt \"Calibri Light\";\n" "background-color: rgb(0, 170, 255);")
        self.save_model_button.setGeometry(QtCore.QRect(90, 380, 300, 20))
        self.save_model_button.setText("Save")
        self.save_model_button.setVisible(True)
        self.save_model_button.clicked.connect(self.save_model_thread)

    def save_model_and_hist(self):
        """
        creating saving model and history option objects
        """
        self.build_label.setVisible(False)
        self.save_model_label = QtWidgets.QLabel(self.build_model_scene)
        self.save_model_label.setGeometry(QtCore.QRect(90, 300, 300, 20))
        self.save_model_label.setStyleSheet("font: 25 12pt \"Calibri Light\";")
        self.save_model_label.setObjectName("save_model_label")
        self.save_model_label.setText("Insert model name:")
        self.save_model_label.setVisible(True)
        self.save_model_lineEdit = QtWidgets.QLineEdit(self.build_model_scene)
        self.save_model_lineEdit.setGeometry(QtCore.QRect(90, 340, 300, 20))
        self.save_model_lineEdit.setObjectName("save_model_lineEdit")
        self.save_model_lineEdit.setVisible(True)
        self.save_model_button = QtWidgets.QPushButton(self.build_model_scene)
        self.save_model_button.setStyleSheet("font: 25 14pt \"Calibri Light\";\n" "background-color: rgb(0, 170, 255);")
        self.save_model_button.setGeometry(QtCore.QRect(90, 380, 300, 20))
        self.save_model_button.setText("Save Model & Model Summary")
        self.save_model_button.setVisible(True)
        self.save_model_button.clicked.connect(self.save_model_thread_file_and_summary)

    def save_model_thread(self):
        """
        saving the created model
        """
        self.label_load_gif = QtWidgets.QLabel(self.build_model_scene)
        self.label_load_gif.setGeometry(530, 380, 50, 50)
        self.animation_load = QMovie("Images/loading_gif.gif")
        self.label_load_gif.setMovie(self.animation_load)
        self.animation_load.start()
        self.flag_save_model=True
        if not self.save_model_lineEdit.text():
            self.save_model_lineEdit.setStyleSheet("border: 1.5px solid red;")
            self.flag_save_model = False
        else:
            self.save_model_lineEdit.setStyleSheet("border-color: 1px rgb(0, 0, 0);")
        if self.flag_save_model:
            self.label_load_gif.setVisible(True)
            self.model_name_str = self.save_model_lineEdit.text()
            self.model_therad.outter.save_model(model_name=self.model_name_str)
            self.label_load_gif.setVisible(False)
            self.msg = QtWidgets.QMessageBox(self.scene_model_settings)
            self.msg.setGeometry(QtCore.QRect(430, 310, 50, 20))
            self.msg.setWindowIcon(QtGui.QIcon("Images/logo.PNG"))
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setText("Model successfully saved!")
            self.msg.setWindowTitle("Information")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            res = self.msg.clickedButton()
            if res.text() == "OK":
                self.build_model_scene.setVisible(False)
                self.go_home()

    def save_model_thread_file_and_summary(self):#TODO:SPLIT AND MOVE
        self.label_load_gif = QtWidgets.QLabel(self.build_model_scene)
        self.label_load_gif.setGeometry(400, 370, 50, 50)
        self.animation_load = QMovie("Images/loading_gif.gif")
        self.label_load_gif.setMovie(self.animation_load)
        self.animation_load.start()
        self.flag_save_model_hist=True
        if not self.save_model_lineEdit.text(): #if no name was inserted
            self.save_model_lineEdit.setStyleSheet("border: 1.5px solid red;")
            self.flag_save_model_hist = False
        else:
            self.save_model_lineEdit.setStyleSheet("border-color: 1px rgb(0, 0, 0);")
        if self.flag_save_model_hist:
            self.label_load_gif.setVisible(True)
            self.model_therad.outter.save_model(model_name=self.save_model_lineEdit.text())
            self.gui_services.save_model_summary(self.model_therad.outter.model,self.save_model_lineEdit.text())
            self.label_load_gif.setVisible(False)
            self.msg = QtWidgets.QMessageBox(self.scene_model_settings)
            self.msg.setGeometry(QtCore.QRect(430, 310, 50, 20))
            self.msg.setWindowIcon(QtGui.QIcon("Images/logo.PNG"))
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setText("Model and model summary successfully saved!")
            self.msg.setWindowTitle("Information")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.exec_()
            res = self.msg.clickedButton()
            if res.text() == "OK":
                self.build_model_scene.setVisible(False)
                self.go_home()

    def init_build_model_frame(self):
        """
        building model frame UI
        """
        self.scene_model_settings.setVisible(False)
        self.build_model_scene = QtWidgets.QFrame(self.frame)
        self.build_model_scene.setGeometry(QtCore.QRect(200, 200, 781, 521))
        self.build_model_scene.setStyleSheet("gridline-color: rgb(0, 255, 0);")
        self.build_model_scene.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.build_model_scene.setFrameShadow(QtWidgets.QFrame.Raised)
        self.build_model_scene.setObjectName("build_model_scene")
        self.log_plainTextEdit = QtWidgets.QPlainTextEdit(self.build_model_scene)
        self.log_plainTextEdit.setGeometry(QtCore.QRect(90, 30, 300, 250))
        self.plot_layout_frame = QtWidgets.QFrame(self.build_model_scene)
        self.plot_layout_frame.setGeometry(QtCore.QRect(400, 10, 300, 317))
        self.plot_layout_frame.setStyleSheet("gridline-color: rgb(0, 255, 0);")
        self.plot_layout_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plot_layout_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plot_layout_frame.setObjectName("plot_layout_frame")
        self.plot_layout_frame.setVisible(True)
        self.plot_build_model_layout = QtWidgets.QGridLayout(self.plot_layout_frame)
        self.plot_build_model_layout.setGeometry(QtCore.QRect(450, 0, 400, 317))
        self.plot_build_model_layout.setObjectName("plot_build_model_layout")
        self.graphWidget_build_model = pg.PlotWidget()
        self.graphWidget_build_model.setBackground('w')
        self.graphWidget_build_model.setTitle("Model loss")
        self.graphWidget_build_model.setLabel('left', 'Loss')
        self.graphWidget_build_model.setLabel('bottom', 'Epoch')
        self.plot_build_model_layout.addWidget(self.graphWidget_build_model, 2, 1)
        self.graphWidget_build_model.addLegend()
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(12)
        self.log_plainTextEdit.setFont(font)
        self.log_plainTextEdit.setObjectName("log_plainTextEdit")
       # self.log_plainTextEdit.horizontalScrollBar().setSliderDown(True)

        self.log_plainTextEdit.setPlainText("Starting build model procedure...\n\n")

        self.log_plainTextEdit.setReadOnly(True)
        self.build_model_scene.setVisible(True)
        self.plot_layout_frame.setVisible(True)
        self.loading_gif_build_model()

    def loading_gif_build_model(self):
        """
        creating build model gif and configure settings
        """
        self.label_load_gif = QtWidgets.QLabel(self.build_model_scene)
        self.build_label = QtWidgets.QLabel(self.build_model_scene)
        self.build_label.setGeometry(370, 310, 150, 50)
        self.build_label.setStyleSheet("font: 25 14pt \"Calibri Light\";")
        self.build_label.setText("Building model...")
        self.build_label.setVisible(True)
        self.label_load_gif.setGeometry(420, 360, 50, 50)
        self.animation_load = QMovie("Images/black_loading.gif")
        self.label_load_gif.setMovie(self.animation_load)
        self.animation_load.start()
        self.label_load_gif.setVisible(True)

    def validate_model_settings(self):
        """
        validation model settings
        """
        flag = True
        if not self.batch_size_line.text():
            self.batch_size_line.setStyleSheet("border: 1.5px solid red;")
            flag = False
        else:
            self.batch_size_line.setStyleSheet("border-color: 1px rgb(0, 0, 0);")
        if not self.epoch_number_line.text():
            self.epoch_number_line.setStyleSheet("border: 1.5px solid red;")
            flag = False
        else:
            self.epoch_number_line.setStyleSheet("border-color: 1px rgb(0, 0, 0);")
        if not self.filter_number_line.text():
            self.filter_number_line.setStyleSheet("border: 1.5px solid red;")
            flag = False
        else:
            self.filter_number_line.setStyleSheet("border-color: 1px rgb(0, 0, 0);")
        if flag:
            temp_flag = True
            if int(self.batch_size_line.text()) < 0:  # batch size must be positive number
                self.batch_size_line.setStyleSheet("border: 1.5px solid red;")
                self.model_settings_validate_msg("Batch size must be a positive number.")
                self.batch_size_line.setStyleSheet("border-color: 1px rgb(0, 0, 0);")
                temp_flag = False
            if int(self.epoch_number_line.text()) < 0:  # epoch number must be positive number
                self.epoch_number_line.setStyleSheet("border: 1.5px solid red;")
                self.model_settings_validate_msg("Epoch must be a positive number.")
                self.epoch_number_line.setStyleSheet("border-color: 1px rgb(0, 0, 0);")
                temp_flag = False
            if int(self.filter_number_line.text()) not in range(32, 350):
                self.filter_number_line.setStyleSheet("border: 1.5px solid red;")
                self.model_settings_validate_msg("Filter number must be between 32 to 350.")
                self.filter_number_line.setStyleSheet("border-color: 1px rgb(0, 0, 0);")
                temp_flag = False
            if temp_flag:
                self.start_model_settings()

    def model_settings_validate_msg(self, str):
        """
        messages validation
        :param str:
        """
        self.msg = QtWidgets.QMessageBox(self.scene_model_settings)
        self.msg.setGeometry(QtCore.QRect(430, 310, 50, 20))
        self.msg.setWindowIcon(QtGui.QIcon("Images/logo.PNG"))
        self.msg.setIcon(QtWidgets.QMessageBox.Warning)
        self.msg.setText(str)
        self.msg.setWindowTitle("Warning")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()

    def logout(self):
        """
        log out from system
        """
        self.user_main_gui.setVisible(False)
        self.operation_list = []
        self.parent().frame.show()
        self.parent().show()
        self.parent().frame.setVisible(True)
        self.close()
