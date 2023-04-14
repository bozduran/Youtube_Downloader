
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import platform
import sys


from pytube import YouTube, Playlist

import Download as dw
import converter as cv

save_path = ''
INITIAL = '/'
CURRENT_WORKING_DIRECTORY = ''


def update_current_working_directory():
    global INITIAL, CURRENT_WORKING_DIRECTORY ,save_path

    if platform.system() == 'Windows':
        path = os.path.expanduser('~\Downloads')
        INITIAL = '\\'
    else:
        path = os.path.expanduser('~/Downloads')

    try:
        os.mkdir(path + INITIAL + 'Youtube Video Downloads')
    except:
        print("")

    path = path + INITIAL + 'Youtube Video Downloads'
    save_path = CURRENT_WORKING_DIRECTORY = path
    return path


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        update_current_working_directory()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(438, 260)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setBold(True)
        font.setWeight(75)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 3)
        self.convert_to_mp3_chekbox = QtWidgets.QCheckBox(self.centralwidget)
        self.convert_to_mp3_chekbox.setObjectName("convert_to_mp3_chekbox")
        self.gridLayout.addWidget(self.convert_to_mp3_chekbox, 1, 0, 1, 1)
        self.download_playlist_chekbox = QtWidgets.QCheckBox(self.centralwidget)
        self.download_playlist_chekbox.setObjectName("download_playlist_chekbox")
        self.gridLayout.addWidget(self.download_playlist_chekbox, 1, 1, 1, 2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)
        self.save_To_Folder_Text_Label = QtWidgets.QLabel(self.centralwidget)
        self.save_To_Folder_Text_Label.setObjectName("save_To_Folder_Text_Label")
        self.gridLayout.addWidget(self.save_To_Folder_Text_Label, 3, 0, 1, 2)
        self.save_folder_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_folder_button.setObjectName("save_folder_button")
        self.gridLayout.addWidget(self.save_folder_button, 3, 2, 1, 1)
        self.download_button = QtWidgets.QPushButton(self.centralwidget)
        self.download_button.setObjectName("download_button")
        self.gridLayout.addWidget(self.download_button, 4, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 438, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.save_To_Folder_Text_Label.setText(update_current_working_directory())

        self.download_button.clicked.connect(self.download_video)
        self.save_folder_button.clicked.connect(self.choose_save_folder)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Youtube downloader"))
        self.lineEdit.setText(_translate("MainWindow", "Insert link here"))
        self.convert_to_mp3_chekbox.setText(_translate("MainWindow", "Convert to Mp3"))
        self.download_playlist_chekbox.setText(_translate("MainWindow", "Download whole playlist"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.save_To_Folder_Text_Label.setText(_translate("MainWindow", update_current_working_directory()))
        self.save_folder_button.setText(_translate("MainWindow", "Save folder"))
        self.download_button.setText(_translate("MainWindow", "Download"))

    def set_label(self,string):
        self.label.setText(string)
    def download_video(self, MainWindow):

        global CURRENT_WORKING_DIRECTORY
        link = self.lineEdit.text()
        dw.path = CURRENT_WORKING_DIRECTORY
        cv.INITIAL = dw.INITIAL = INITIAL
        print(link)

        if self.download_playlist_chekbox.isChecked():
            self.set_label(Playlist(link).title)

            path_to_folder = dw.on_click_download_playlist_as_video_button(link,
                                                                           int(self.convert_to_mp3_chekbox.isChecked()))

            os.remove(path_to_folder + '/links.txt')
        else:
            print(CURRENT_WORKING_DIRECTORY)
            dw.download_video_as_mp3(link, CURRENT_WORKING_DIRECTORY)

        print(f'{dw.Bcolors.OKGREEN}Complete{dw.Bcolors.ENDC}')


    def choose_save_folder(self, MainWindow):
        global save_path, CURRENT_WORKING_DIRECTORY
        CURRENT_WORKING_DIRECTORY = save_path = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Folder')
        self.save_To_Folder_Text_Label.setText(save_path)
        print(save_path)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

