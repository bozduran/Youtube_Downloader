import re
import traceback

import pytube
from pytube import YouTube, Playlist
from pytube.cli import on_progress
from pytube.exceptions import VideoUnavailable
import requests
import os
from pydub import AudioSegment

import mylogger
import converter

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


def clear_illegal_characters(text):
    invalid = '/'
              #'<>:"/\|?*'
    mylogger.logger.warning(f"Change illegal characters in text: {text}")

    for char in invalid:
        text = text.replace(char, '')

    return text


def check_url(link):

    try:
        yt = YouTube(link)
        mylogger.logger.info(f'Video {link} is available.')

    except VideoUnavailable:
        mylogger.logger.critical(f'Video {link} is unavailable, skipping.')
    else:
        return link


def check_ff_playlist_is_playlist(playlist: object) -> object:
    try:
        mylogger.logger.info(f"Downloading playlist {playlist.title}.")
        return True
    except:
        download_video_file(playlist, path=path)
        return False


def create_folder(path_for_folder=''):
    if os.path.exists(path_for_folder):
        mylogger.logger.info(f"Path already exists {path_for_folder}.")
        return
    try:
        os.mkdir(path_for_folder, 0o777)
        mylogger.logger.info(f"Path created {path_for_folder}.")
    except Exception:
        mylogger.logger('create_folder:', traceback.print_exc())

def download_thumbnail(youTube):
    mylogger.logger.info("Trying to download thumbnail.")
    thumbnail_link = youTube.thumbnail_url
    file_name = f'{clear_illegal_characters(youTube.title)}'
    img_data = requests.get(thumbnail_link).content
    create_folder('Thumbnails')
    filename = 'Thumbnails/' + file_name + '.jpg'

    with open(filename, 'wb') as handler:
        handler.write(img_data)

def file_name_formatter(file_name):
    mylogger.logger.info("filename_formatter: {}".format(file_name))
    return clear_illegal_characters(file_name)

def download_video_file(link, numberOfVideo=1, outOf=1, path=path):
    check_url(link)
    yt = YouTube(link, on_progress_callback=on_progress)
    download_thumbnail(yt)
    #video_filename = file_name_formater(yt.title)
    mylogger.logger.info(f' {Bcolors.BOLD}Downloading: {yt.title} viewed: {yt.views} times.{Bcolors.ENDC}')
    filtered_stream = yt.streams.filter(progressive=True).order_by('resolution').desc()
    filtered_stream.get_highest_resolution().download(output_path=path)
    mylogger.logger.info(f' {Bcolors.BOLD}Download of video {yt.title} complete.{Bcolors.ENDC}')
    return f'{path}{INITIAL}{clear_illegal_characters(yt.title)}.mp4'

def download_video_as_mp3(url, destination_folder):
    youtube = YouTube(url,  on_progress_callback=on_progress)

    # Get the audio stream and download it
    audio_stream = youtube.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=destination_folder)

    downloaded_file_path = os.path.join(destination_folder, clear_illegal_characters(audio_stream.default_filename))
    sound = AudioSegment.from_file(downloaded_file_path)
    mp3_file_path = os.path.splitext(downloaded_file_path)[0] + '.mp3'
    sound.export(mp3_file_path, format='mp3')
    os.remove(downloaded_file_path)

    mylogger.logger.info(f"Downloaded and converted {url} to {destination_folder}")

def download_videos_of_playlist(playlist, already_downloaded, destination_path, AUDIO=0):
    video_count = len(playlist)
    for i, video in enumerate(playlist, start=1):
        if video not in already_downloaded:
            mylogger.logger.info(f'{Bcolors.OKBLUE}Downloading {i} out of {video_count}{Bcolors.ENDC}')
            try:
                with open(destination_path + INITIAL + "links.txt", 'a+') as file:
                    if AUDIO:
                        download_video_as_mp3(video, destination_path)
                    else:
                        download_video_file(video, i, video_count, destination_path)
                    file.write(f'{video}\n')
            except Exception:
                mylogger.logger.critical("download_videos_of_playlist:", traceback.print_exc())
        else:
            mylogger.logger.info(f"already_downloaded:{video}")


def on_click_download_playlist_as_video_button(link,audio):
    playlist = Playlist(link)
    if check_ff_playlist_is_playlist(playlist) == False:
        return
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")  #
    playlist_name = playlist.title
    full_path = f'{path}{INITIAL}{clear_illegal_characters(playlist_name)}'
    mylogger.logger.info('Downloaded playlist will be saved: ',full_path)
    create_folder(full_path)
    mylogger.logger.info("Sequence to read already downloaded files in function on_click_download_playlist_as_video_button: ")
    file = open_file_name(full_path)
    already_downloaded = read_downloaded_name(file)
    mylogger.logger.info("End of sequence to read already downloaded files in function on_click_download_playlist_as_video_button")
    download_videos_of_playlist(playlist, already_downloaded, full_path, audio)
    return full_path

def download(link, download_whole_playlist):
    check_url(link)

def read_downloaded_name(file):
    mylogger.logger.info("read_downloaded_name")
    return_list = []
    for x in file:
        return_list.append(x)

    return return_list

def open_file_name(path):
    mylogger.logger.info("open_file_name")
    try:
        file = open((path + INITIAL + "links.txt"), 'a+')
        return file
    except Exception:
        traceback.print_exc()
