import re
import traceback

from pytube import YouTube, Playlist
from pytube.cli import on_progress
from pytube.exceptions import VideoUnavailable
import requests
import os

downloaded_files = []
# import shutlib
path = ''
INITIAL = '/'


class Bcolors:
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


def clear_illegal_caracters(text):
    invalid = '<>:"/\|?*'

    for char in invalid:
        text = text.replace(char, '')
    return text


def check_url(link):
    print('Checking link.')
    try:
        yt = YouTube(link)
    except VideoUnavailable:
        print(f'Video {link} is unavaialable, skipping.')
        exit(1)
    else:
        return link


def check_If_playlistIs_playlist(playlist):
    try:
        print(f'Downloading playlist: {playlist.title}')
        return True
    except:
        download_video_file(playlist, path=path)
        return False


def create_folder(path_for_folder=''):
    if os.path.exists(path_for_folder):
        return
    try:
        os.mkdir(path_for_folder, 0o777)
    except Exception:
        traceback.print_exc()


def download_video_file(link, numberOfVideo=1, outOf=1, path=path):
    yt = YouTube(link, on_progress_callback=on_progress)
    thumbnail_link = yt.thumbnail_url
    video_filename = yt.title.replace('|', '')
    img_data = requests.get(thumbnail_link).content
    create_folder('Thumbnails')
    filename = 'Thumbnails/' + video_filename + '.jpg'

    with open(filename, 'wb') as handler:
        handler.write(img_data)

    print(f' ' + Bcolors.BOLD + 'Downloading: ', yt.title, '~ viewed', yt.views,
          'times.', Bcolors.ENDC)
    filtered_stream = yt.streams.filter(progressive=True).order_by('resolution').desc()

    filtered_stream.get_highest_resolution().download(output_path=path)
    print(Bcolors.OKGREEN + f'Download of video {yt.title} complete.' + Bcolors.ENDC)
    return path + INITIAL + video_filename + '.mp4'


def download_videos_of_playlist(playlist, alreadyDownloaded, fullPath, AUDIO=0):
    i = 0
    for video in playlist:
        i += 1
        if video not in alreadyDownloaded:
            print(f'Downloading {i} out of {len(playlist)}')
            try:
                file = open((fullPath + INITIAL + "links.txt"), 'a+')
                if (AUDIO == 1):
                    download_video_file(video, i, len(playlist.videos), fullPath)
                else:
                    download_video_file(video, i, len(playlist.videos), fullPath)
                text = str(video) + str('\n')
                file.write(text)
                file.close()
            except Exception:
                traceback.print_exc()


def on_clickdownload_playlistas_video_button(link):
    playlist = Playlist(link)
    if check_If_playlistIs_playlist(playlist) == False:
        return
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")  #
    playlist_name = playlist.title
    full_path = path + INITIAL + playlist_name.replace(':', '')
    print(full_path)
    create_folder(full_path)
    file = open_file_name(full_path)
    already_downloaded = read_downloaded_name(file)
    download_videos_of_playlist(playlist, already_downloaded, full_path, AUDIO=0)
    return full_path


def download(link, download_whole_playlist):
    check_url(link)


def read_downloaded_name(file):
    return_list = []
    for x in file:
        return_list.append(x)

    return return_list


def open_file_name(path):
    try:
        file = open((path + INITIAL + "links.txt"), 'a+')
        return file
    except Exception:
        traceback.print_exc()
