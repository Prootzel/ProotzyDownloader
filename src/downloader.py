from pytube import YouTube, Playlist
from PIL import Image
import requests
from io import BytesIO
import re
import moviepy.editor as mpConverter
import os
import threading

def getAllVideoInfo (source : YouTube) -> dict[str, str]:
    """
    Get all video info
    ------------------------------------------------------------------------------------\n
    source : source youtube video
    ------------------------------------------------------------------------------------\n                                                                  \n
    return : title, author, length, rating and viewcount as strings
    """
    return{
        (f"title  :  {source.title}"),
        (f"author :  {source.author}"),
        (f"length :  {source.length}"),
        (f"rating :  {source.rating}"),
        (f"views  :  {source.views}"),
    }

def cleanTitle (title : str) -> str:
    """
    Regex utility to clean up any string to be able to be a filename on NTFS drives     \n
    ------------------------------------------------------------------------------------\n
    title : input to be cleaned up                                                      \n
    ------------------------------------------------------------------------------------\n
    return : cleaned string of title                                                    \n
    ------------------------------------------------------------------------------------\n
    DONE
    """
    titleCleaner = re.compile('[|><\\/*"]:?')
    return titleCleaner.sub('', title)

def downloadVideoOrAudio (url : str, printInfo : bool = True, fileFormat : str = ".mp4", audio : bool = True, fileName = "", filePath = "", toMp = False, filePrefix : str = "", path : str = "audio") -> bool:
    """
    Download the best quality audio/video from a youtube stream                         \n
    ------------------------------------------------------------------------------------\n
    source : Source youtube stream                                                      \n
    printInfo : Print the video information to console                                  \n
    fileFormat : File format to append                                                  \n
    audio : If true, only rips audio; if false, rips video and audio                    \n
    toMp : converts to mp3 file if true                                                 \n
    filePrefix : string to attach before the file; used for adding index for playlist   \n
    ------------------------------------------------------------------------------------\n
    return : currently returns true, future updates will return false in case of error  \n
    ------------------------------------------------------------------------------------\n
    TODO: clean up (like a lot), improve .mp3 performance
    """

    source = YouTube(url=url)

    if(printInfo):
        print(getAllVideoInfo(source))


    if(audio):
        stream = source.streams.get_audio_only()
    else:
        stream = source.streams.get_highest_resolution()
    if(fileName == ""):
        title : str = cleanTitle(source.title)

        
    else:
        title : str = cleanTitle(fileName)
    

    if(toMp):
        print("Converting video")
        vidPath = f"{os.getcwd()}\\{filePath}\\{title}{fileFormat}"
        audPath = stream.download(output_path = filePath, filename=f"{filePrefix}{title}{fileFormat}")
        vid = mpConverter.AudioFileClip(vidPath)
        vid.write_audiofile(audPath)
        vid.close()
    else:
        stream.download(output_path = filePath, filename=f"{filePrefix}{title}{fileFormat}")
    return True
    

def downloadVideoThumbnail (url : str, printInfo : bool = True, fileFormat : str = ".png", showAfter : bool = True) -> bool:
    """
    Download the highest quality video thumbnail                                        \n
    ------------------------------------------------------------------------------------\n
    url : string source url                                                             \n
    printInfo : if true, prints video info to console                                   \n
    fileFormat : string for file ending                                                 \n
    showAfter : if true, open up the os's default image gallery with the thumbnail      \n
    ------------------------------------------------------------------------------------\n
    return : true for now, used for errors in the future                                \n
    ------------------------------------------------------------------------------------\n
    DONE
    """
    source = YouTube(url)
    
    thumbnail = Image.open(BytesIO(requests.get(source.thumbnail_url).content))
    
    title : str = cleanTitle(source.title)

    thumbnail.save(fp = f"{os.path.dirname(os.path.abspath(__file__))}\\thumbnails\\{title}{fileFormat}")
    if(showAfter): 
        thumbnail.show()
    return True



def downloadPlaylist(url : str, printInfo : bool = True, audioOnly : bool = False, addIndex : bool = False, toMp : bool = False) -> bool:
    """
    Downloads an entire playlist                                                        \n
    ------------------------------------------------------------------------------------\n
    url : string source url                                                             \n
    audioOnly : if true, only downloads audio (.mp4)                                    \n
    addIndex : if true, prefixes all files in the format "{index + 1}. "                \n
    toMp : convert to .mp3 files after the download has finished                        \n
    ------------------------------------------------------------------------------------\n
    return : true for now, false in case of an error in a future update                 \n
    ------------------------------------------------------------------------------------\n
    TODO: improve .mp3 performance, add more ways of indexing maybe?
    """
    threadLimit = 64
    playlist = Playlist(url)
    vids = playlist.video_urls
    playlistPath = f"{os.getcwd()}\\playlists\\{cleanTitle(playlist.title)}"


    if(not os.path.exists(playlistPath)):
        os.makedirs(playlistPath)
    if(addIndex):
        
        for i, cur in enumerate(vids):
            if(threading.active_count() > threadLimit):
                ...
            try:
                threading.Thread(target = lambda : downloadVideoOrAudio(url = cur, printInfo = True, audio = audioOnly, toMp=toMp, filePrefix=f"{i+1}. ", filePath=playlistPath)).run()

            except KeyboardInterrupt:
                exit()
            except Exception as e:
                print(f"Error reading {url}")
                print(e)
    else:
        for i, cur in enumerate(vids):
            if(threading.active_count() > threadLimit):
                ...
            threading.Thread(target = lambda : downloadVideoOrAudio(url = cur, printInfo = True, audio = audioOnly, toMp=toMp, filePath=playlistPath)).run()
    return True