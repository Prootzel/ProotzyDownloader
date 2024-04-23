from pytube import YouTube, Playlist
from PIL import Image, ImageGrab
import requests
from io import BytesIO
import re
import moviepy.editor as mpConverter
import os
import threading
from time import sleep
#import gui_classes as gui

#applicationGUI = gui.Application()


#videoPath : str = input("Enter youtube URL > ")

#filePath = f"__file__"

#getOnlyMusic : bool = input("Grab only music stream (y/n)? > ") == "y"

#vid = YouTube(videoPath)

def printVideoInfo (source : YouTube):
    print(f"Title  :  {source.title}")
    print(f"Author :  {source.author}")
    print(f"Length :  {source.length}")
    print(f"Rating :  {source.rating}")
    print(f"Views  :  {source.views}")

def cleanTitle (title : str) -> str:
    titleCleaner = re.compile('[|><\\/*"]:?')
    return titleCleaner.sub('', title)

def downloadVideoOrAudio (url : str, printInfo : bool = True, fileFormat : str = ".mp4", audio : bool = True, fileName = "", filePath = "", toMp = False, filePrefix : str = "") -> bool:
    """
    Download the best quality audio/video from a youtube stream         \n
    source : Source youtube stream                                      \n
    printInfo : Print the video information to console                  \n
    fileFormat : File format to append                                  \n
    audio : If true, only rips audio; if false, rips video and audio    \n
    uwu
    """

    source = YouTube(url=url)

    if(printInfo):
        printVideoInfo(source)


    if(audio):
        stream = source.streams.get_audio_only()
    else:
        stream = source.streams.get_highest_resolution()
    if(fileName == ""):
        title : str = cleanTitle(source.title)

        
    else:
        title : str = cleanTitle(fileName)
    
    stream.download(output_path = filePath, filename=f"{filePrefix}{title}{fileFormat}")

    if(toMp):
        vidPath = f"{os.getcwd()}\\audio\\{title}{fileFormat}"
        audPath = f"{os.getcwd()}\\audio\\{title}.mp3"
        vid = mpConverter.AudioFileClip(vidPath)
        vid.write_audiofile(audPath)
        vid.close()
        os.remove(vidPath)
    return True
    

def downloadVideoThumbnail (url : str, printInfo : bool = True, fileFormat : str = ".png", showAfter : bool = True) -> bool:
    source = YouTube(url)
    
    if(printInfo):
        printVideoInfo(source)
    response = requests.get(source.thumbnail_url)
    thumbnail = Image.open(BytesIO(requests.get(source.thumbnail_url).content))
    
    title : str = cleanTitle(source.title)

    thumbnail.save(fp = f"{os.path.dirname(os.path.abspath(__file__))}\\thumbnails\\{title}{fileFormat}")
    if(showAfter): 
        thumbnail.show()
    # \\{source.title}{fileFormat}
    return True



def downloadPlaylist(url : str, printInfo : bool = True, audioOnly : bool = False, addIndex : bool = False, toMp : bool = False) -> bool:
    threadLimit = 64
    playlist = Playlist(url)
    vids = playlist.video_urls
    print(playlist.video_urls)
    playlistPath = f"{os.getcwd()}\\playlists\\{cleanTitle(playlist.title)}"
    if(not os.path.exists(playlistPath)):
        os.makedirs(playlistPath)
    if(addIndex):
        for i, cur in enumerate(vids):
            if(threading.active_count() > threadLimit):
                ...
            try:
                threading.Thread(target = lambda : downloadVideoOrAudio(url = cur, printInfo = True, audio = audioOnly, toMp=toMp, filePrefix=f"{i+1}. ", filePath=playlistPath)).run()
            except:
                print(f"Error reading {url}")
    else:
        for i, cur in enumerate(vids):
            if(threading.active_count() > threadLimit):
                ...
            threading.Thread(target = lambda : downloadVideoOrAudio(url = cur, printInfo = True, audio = audioOnly, toMp=toMp, filePath=playlistPath)).run()
    return True