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
    print(path)
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
