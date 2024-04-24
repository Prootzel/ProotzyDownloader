import customtkinter as ctk
import downloader as downloader

class Application(ctk.CTk):
    """
    Base application class                                  \n
    --------------------------------------------------------\n
    __init__(self) -> None: Instantiates a GUI              \n 
    --------------------------------------------------------\n
    DONE
    """

    def __init__(self):
        """
        GUI Initialiser                                         \n
        --------------------------------------------------------\n
        self: self                                              \n
        --------------------------------------------------------\n
        return : none                                           \n
        --------------------------------------------------------\n
        TODO: something I forgor 💀💀💀
        """

        super().__init__()

        self.playlistVideoTabView = PlaylistVideoTabView(master = self)
        self.playlistVideoTabView.grid(row = 0, column = 0, padx = 20, pady = 20)

        self.title("Prootzy Youtube Downloader v1.0")

        self.config(height=720, width=1280)

        try:
            self.mainloop()
        except KeyboardInterrupt:
            exit()
        exit()


class PlaylistVideoTabView(ctk.CTkTabview):
    """
    Initialise all tabviews\n
    --------------------------------------------------------\n
    __init__(self, master, **kwargs) -> None: Class initialiser\n
    --------------------------------------------------------\n
    DONE
    """

    frames : list[ctk.CTkFrame] = []
    def __init__(self, master, **kwargs):
        """
        Tabview Initialiser                                     \n
        --------------------------------------------------------\n
        self: self                                              \n
        master: master window (CTk.Frame)                       \n
        **kwargs: keyword args for CTk.Frame base               \n
        --------------------------------------------------------\n
        return : none                                           \n
        --------------------------------------------------------\n
        TODO: something I forgor 💀💀💀
        """
        super().__init__(master, **kwargs)


        self.add("Video")
        self.frames.append(VideoAudioDownloader(master = self.tab("Video")))
        self.frames[0].grid(row = 0, column = 0)

        self.add("Audio")
        self.frames.append(VideoAudioDownloader(master = self.tab("Audio"), isAudioDownloader=True))
        self.frames[1].grid(row = 0, column = 0)


        self.add("Playlist")
        self.frames.append(PlaylistDownloader(master = self.tab("Playlist")))
        self.frames[2].grid(row = 0, column = 0)
        
        self.add("Thumbnail")
        self.frames.append(ThumbnailDownloader(master = self.tab("Thumbnail")))
        self.frames[3].grid(row = 0, column = 0)


class ThumbnailDownloader(ctk.CTkFrame):
    """
    Thumbnail downloader GUI class\n
    --------------------------------------------------------\n
    DONE
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.sourceVar = ctk.StringVar()

        
        self.path = ctk.StringVar()

        self.fileFormat = ctk.StringVar(value = ".png")

        self.showFileAfter = ctk.BooleanVar(value = True)

        gridMaster = ctk.CTkFrame(self, width=400, height = 200)
        ctk.CTkLabel(gridMaster, width=100, height = 10, text = "URL").grid(row = 0, column = 0)
        self.sourceTextBox = ctk.CTkEntry(gridMaster, width=300, height = 10, corner_radius = 5, textvariable = self.sourceVar)
        self.sourceTextBox.grid(row = 0, column = 1, pady = 5)





        imageFileFormats = [".png", ".jpg"]
        ctk.CTkLabel(gridMaster, width=100, height = 10, text = "File format").grid(row = 2, column = 0)
        self.fileTypeSelector = ctk.CTkOptionMenu(gridMaster, width=300, height = 10, corner_radius=5, values=imageFileFormats, variable=self.fileFormat)
        self.fileTypeSelector.grid(row = 2, column = 1)
        self.fileTypeSelector.grid(row = 2, column = 1, pady = 5)


        ctk.CTkLabel(gridMaster, width=100, height = 10, text = "Show file after").grid(row = 3, column = 0)
        self.showFileAfterBox = ctk.CTkCheckBox(gridMaster, width=10, height=10, corner_radius=5, variable=self.showFileAfter, text="")
        self.showFileAfterBox.grid(row = 3, column = 1)
        self.showFileAfterBox.grid(row = 3, column = 1, pady = 5)

            


        self.convertButton = ctk.CTkButton(self,corner_radius=5, text="Download Thumbnail", 
        command=lambda : downloader.downloadVideoThumbnail(url = self.sourceVar.get(), fileFormat=self.fileFormat.get()))

        gridMaster.grid(row = 0, column = 0)
        self.convertButton.grid(row = 2, column = 0, pady = 10)

class PlaylistDownloader(ctk.CTkFrame):
    """
    Playlist downloader GUI class \n
    --------------------------------------------------------\n
    RETURN
    --------------------------------------------------------\n
    DONE
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.sourceVar = ctk.StringVar()

        
        self.index = ctk.BooleanVar(value=True)

        self.toMp = ctk.BooleanVar(value=False)

        self.onlyAudio = ctk.BooleanVar(value = False)

        gridMaster = ctk.CTkFrame(self, width=400, height = 200)
        ctk.CTkLabel(gridMaster, width=100, height = 10, text = "URL").grid(row = 0, column = 0)
        self.sourceTextBox = ctk.CTkEntry(gridMaster, width=300, height = 10, corner_radius = 5, textvariable = self.sourceVar)
        self.sourceTextBox.grid(row = 0, column = 1, pady = 5)



        ctk.CTkLabel(gridMaster, width=100, height = 10, text = "Get only audio").grid(row = 3, column = 0)
        self.onlyAudioBox = ctk.CTkCheckBox(gridMaster, width=10, height=10, corner_radius=5, variable=self.onlyAudio, text="")
        self.onlyAudioBox.grid(row = 3, column = 1, pady = 5)

        ctk.CTkLabel(gridMaster, width=100, height = 10, text = "Add index to file name").grid(row = 4, column = 0)
        self.indexBox = ctk.CTkCheckBox(gridMaster, width=10, height=10, corner_radius=5, variable=self.index, text="")
        self.indexBox.grid(row = 4, column = 1, pady = 5)

        self.convertButton = ctk.CTkButton(self,corner_radius=5, text="Download", 
        command = lambda : downloader.downloadPlaylist(url = self.sourceVar.get(), audioOnly=self.onlyAudio.get(), 
        printInfo = True, addIndex=self.index.get()))



        gridMaster.grid(row = 0, column = 0)
        self.convertButton.grid(row = 2, column = 0, pady = 10)


class VideoAudioDownloader(ctk.CTkFrame):
    def __init__(self, master, isAudioDownloader : bool = False, **kwargs):
        super().__init__(master, **kwargs)

        self.sourceVar = ctk.StringVar()

        
        self.path = ctk.StringVar()

        self.fileFormat = ctk.StringVar(value = ".mp4")

        self.isAudioDownloader = isAudioDownloader

        if(isAudioDownloader):
            self.AudioSetup()
        else:
            self.VideoSetup()

    def AudioSetup(self):
        self.convertToMp = ctk.BooleanVar(value = False)

        gridMaster = ctk.CTkFrame(self, width=400, height = 200)
        ctk.CTkLabel(gridMaster, width=100, height = 10, text = "URL").grid(row = 0, column = 0)
        self.sourceTextBox = ctk.CTkEntry(gridMaster, width=300, height = 10, corner_radius = 5, textvariable = self.sourceVar)
        self.sourceTextBox.grid(row = 0, column = 1, pady = 5)



        ctk.CTkLabel(gridMaster, width=100, height = 10, text = "Convert to mp3").grid(row = 3, column = 0)
        self.convertToMpBox = ctk.CTkCheckBox(gridMaster, width=10, height=10, corner_radius=5, variable=self.convertToMp, text="")
        self.convertToMpBox.grid(row = 3, column = 1, pady = 5)

        self.convertButton = ctk.CTkButton(self,corner_radius=5, text="Convert to Audio", 
        command=lambda : downloader.downloadVideoOrAudio(url = self.sourceVar.get(), audio=True, printInfo=True, fileFormat=self.fileFormat.get(), filePath = "audio\\", toMp = True))

        gridMaster.grid(row = 0, column = 0)
        self.convertButton.grid(row = 2, column = 0, pady = 10)

    def VideoSetup(self):
        gridMaster = ctk.CTkFrame(self, width=400, height = 200)
        ctk.CTkLabel(gridMaster, width=100, height = 10, text = "URL").grid(row = 0, column = 0)
        self.sourceTextBox = ctk.CTkEntry(gridMaster, width=300, height = 10, corner_radius = 5, textvariable = self.sourceVar)
        self.sourceTextBox.grid(row = 0, column = 1, pady = 5)


        self.convertButton = ctk.CTkButton(self,corner_radius=5, text="Convert to Video", 
        command=lambda : downloader.downloadVideoOrAudio(url = self.sourceVar.get(), audio=False, printInfo=True, fileFormat=self.fileFormat.get(), filePath = "video\\"))

        gridMaster.grid(row = 0, column = 0)
        self.convertButton.grid(row = 2, column = 0, pady = 10)

if(__name__=="__main__"):
    Application()