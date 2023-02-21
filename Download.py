import re
import traceback

from pytube import YouTube, Playlist
from pytube.cli import on_progress
from pytube.exceptions import VideoUnavailable
import requests
import os

downloaded_files = []
#import shutlib
path = ''
INITIAL = '/'


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
    print('Yt objcreated')
    thumbnail_link = yt.thumbnail_url
    print('thumbnail_link objcreated')
    video_filename=  yt.title.replace('|','')
    img_data = requests.get(thumbnail_link).content
    createFolder('Thumbnails')#'/Thumbnails/'+
    filename = 'Thumbnails/' + video_filename + '.jpg'

    print('1',filename)
    with open(filename, 'wb') as handler:
        handler.write(img_data)

    print('2')
    print(f' ' + bcolors.BOLD + 'Downloading: ', yt.title, '~ viewed', yt.views,
          'times.',bcolors.ENDC)
    filteredStream = yt.streams.filter(progressive=True).order_by('resolution').desc()

    filteredStream.get_highest_resolution().download(output_path=path)
    #print(bcolors.OKGREEN +f'Download of video {yt.title} complete.'+bcolors.ENDC)
    return path +INITIAL+video_filename + '.mp4'

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
    print('this')
    if chekIfPlaylistIsPlaylist(playlist) == False:
        return
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")  #
    #channelName = playlist.owner  # Chanel owner
    playlistName = playlist.title  # name of playlist
    #fullPath = path + INITIAL + channelName
    #createFolder(fullPath)
    fullPath = path + INITIAL + playlistName.replace(':','')
    print(fullPath)
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

