# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'youtubedownloader.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
import os
import platform
import Download as dw
import converter as cv
save_path = ''

INITIAL = '/'
CURRENT_WORKING_DIRECTORY = ''
downloaded_files = []
#import shutlib
path = ''
INITIAL = '/'

import re
import traceback

from pytube import YouTube, Playlist
from pytube.cli import on_progress
from pytube.exceptions import VideoUnavailable
import requests
import os
import eyed3 as eyed3
from eyed3.id3.frames import ImageFrame
from moviepy.editor import *
INITIAL = '/'

def add_thumbnail(name):
    l = name.split(INITIAL)
    image_name = os.getcwd() + '/Thumbnails/' + l[-1].replace('.mp3','.jpg')
    audiofile = eyed3.load(name)
    if (audiofile.tag == None):
        audiofile.initTag()

    audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(image_name, 'rb').read(), 'image/jpeg')

    audiofile.tag.save()

def folder_to_mp3(path):
    files =[]
    for file in os.listdir(path):
        if file.endswith('.mp4'):
            files.append(path + INITIAL + file)
            print(file)

    for mp4 in files:
        mp_4_to_mp_3(mp4)




def mp_4_to_mp_3(file):
    videoclip = VideoFileClip(file)
    audioclip = videoclip.audio
    mpr3name = file.replace('.mp4', '') + '.mp3'
    audioclip.write_audiofile(mpr3name)
    audioclip.close()
    videoclip.close()
    try:
        print('add thumbnail')
        add_thumbnail(mpr3name)
    except:
        print('Error adding thumbnail.')
    os.remove(file)




class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

fuchsia = '\033[38;2;255;00;255m'  # color as hex #FF00FF
reset_color = '\033[39m'

def clear_ilegal_caracters(text):
    invalid = '<>:"/\|?*'

    for char in invalid:
        text = text.replace(char, '')
    return text

def checkUrl(link):
    print('Checking link.')
    try:
        yt = YouTube(link)
    except VideoUnavailable:
        print(f'Video {link} is unavaialable, skipping.')
        exit(1)
    else:
        return link

def chekIfPlaylistIsPlaylist(playlist):
    try:
        print(f'Downloading playlist: {playlist.title}')
        return True
    except:
        downloadVideoFile(playlist,path = path)
        return False


def createFolder(path=''):
    if os.path.exists(path):
        return
    try:
        os.mkdir(path, 0o777)
    except Exception:
        traceback.print_exc()


def downloadVideoFile(link, numberOfVideo=1, outOf=1, path=path):


    yt = YouTube(link)
    thumbnail_link = yt.thumbnail_url

    img_data = requests.get(thumbnail_link).content
    createFolder('Thumbnails')#'/Thumbnails/'+

    filename = 'Thumbnails/' + yt.title + '.jpg'
    with open(filename, 'wb') as handler:
        handler.write(img_data)


    print(f' ' + bcolors.BOLD + 'Downloading: ', yt.title, '~ viewed', yt.views,
          'times.',bcolors.ENDC)
    filteredStream = yt.streams.filter(progressive=True).order_by('resolution').desc()

    filteredStream.get_highest_resolution().download(output_path=path)
    #print(bcolors.OKGREEN +f'Download of video {yt.title} complete.'+bcolors.ENDC)
    return path +INITIAL+yt.title + '.mp4'

def downloadVideosOfPlaylist(playlist, alreadyDownloaded, fullPath, AUDIO=0):
    i = 0
    for video in playlist:
        i += 1
        if video not in alreadyDownloaded:
            print(f'Downloading {i} out of {len(playlist)}')
            try:
                file = open((fullPath + INITIAL + "links.txt"), 'a+')
                if (AUDIO == 1):
                    downloadVideoFile(video, i, len(playlist.videos), fullPath)
                else:
                    downloadVideoFile(video, i, len(playlist.videos), fullPath)
                text = str(video) + str('\n')
                file.write(text)
                file.close()
            except Exception:
                traceback.print_exc()

def onClickdownloadPlaylistasVideoButton(link):

    playlist = Playlist(link)
    if chekIfPlaylistIsPlaylist(playlist) == False:
        return
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")  #
    channelName = playlist.owner  # Chanel owner
    playlistName = playlist.title  # name of playlist
    fullPath = path + INITIAL + channelName
    createFolder(fullPath)
    fullPath = fullPath + INITIAL + playlistName
    createFolder(fullPath)
    file = openFileName(fullPath)
    alreadyDownloaded = readDownloadedName(file)
    downloadVideosOfPlaylist(playlist, alreadyDownloaded, fullPath, AUDIO=0)
    return fullPath


def download(link,download_whole_playlist ):
    checkUrl(link)










def readDownloadedName(file):
    #print(f'Reading file ')
    returnList = []
    for x in file:
        returnList.append(x)

    return returnList


def openFileName(path):
    #print(f'Opening file {path}')
    try:
        file = open((path + INITIAL + "links.txt"), 'a+')
        return file
    except Exception:
        traceback.print_exc()



def update_CURRENT_WORKING_DIRECTORY():
    global INITIAL , CURRENT_WORKING_DIRECTORY

    path = os.getcwd()

    if platform.system() == 'Windows':
        path = os.path.expanduser('~\Downloads')
        INITIAL = '\\'
    else:
        path = os.path.expanduser('~/Downloads')
    CURRENT_WORKING_DIRECTORY = path
    return path

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
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

        self.save_To_Folder_Text_Label.setText(update_CURRENT_WORKING_DIRECTORY())

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
        self.save_To_Folder_Text_Label.setText(_translate("MainWindow", update_CURRENT_WORKING_DIRECTORY()))
        self.save_folder_button.setText(_translate("MainWindow", "Save folder"))
        self.download_button.setText(_translate("MainWindow", "Download"))

    def download_video(self,MainWindow):
        global CURRENT_WORKING_DIRECTORY
        link = self.lineEdit.text()
        dw.path = CURRENT_WORKING_DIRECTORY
        cv.INITIAL = dw.INITIAL = INITIAL
        print(link)

        if self.download_playlist_chekbox.isChecked():
            path_tofolder = dw.onClickdownloadPlaylistasVideoButton(link)
            if self.convert_to_mp3_chekbox.isChecked():
                cv.mp4tomp3(path_tofolder)
        else:
            file_path = dw.downloadVideoFile(link,path=CURRENT_WORKING_DIRECTORY )
            if self.convert_to_mp3_chekbox.isChecked():
                cv.mp_4_to_mp_3(file_path)
        print('Actions complete.')
        exit(1)




    def choose_save_folder(self,MainWindow):
        global save_path
        save_path = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Folder')
        self.save_To_Folder_Text_Label.setText(save_path)

#pyuic5 -x -o main.py youtubedownloader.ui

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
