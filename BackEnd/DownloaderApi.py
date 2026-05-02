import json
import os
import shutil
import yt_dlp
from BackEnd import file_utils 
from yt_dlp.utils import DownloadError, ExtractorError
from yt_dlp.utils import download_range_func
from UI import LoadingBar as lb



class Downloader:
    def __init__(self, url, selection, file_path, thread=None, clipping=False, start=0, end=0):
        self.url = url 
        self.selection = selection #Selects the download mode
        self.file_path = file_path 
        self.thread = thread #Poooooower to stop the loading bar thread
        self.is_playlist = self.detect_playlist() #Checks if the link is in a playlist
        self.want_playlist_downloaded = False 
        self.start = start #Start of the clip
        self.clipping = clipping #If the user wants to clip
        self.end = end #End of the Clip
        
        self.acceptedFormats = {"video": ["mp4", "mkv", "webm", "avi", "mov"],
                           "audio": ["mp3", "m4a", "aac", "flac", "wav"],
                           "video_audio": ["mp4", "mkv", "webm", "avi", "mov"]}
        
        #Referencing Json
        json_path = file_utils.resource_path("Util/user-experience.json")
        with open(json_path, 'r') as file:
            self.jsoncontrol = json.load(file)
            
        json_path = file_utils.resource_path("Util/default.json")
        with open(json_path, 'r') as file:
            self.defaultJson = json.load(file)
        
            
        #Importing ffmpeg
        ffmpeg_path = os.path.join(os.path.dirname(__file__), "..", "Util", "ffmpeg")
        os.environ["PATH"] += os.pathsep + ffmpeg_path
        print("ffmpeg found:", shutil.which("ffmpeg"))
        
        print(f"Selection: {selection}")
        
        #Cookies and smth else idk (cerificate)
        self.ca_path = file_utils.resource_path("Util/cacert.pem")
        print(self.ca_path)
        os.environ["SSL_CERT_FILE"] = self.ca_path
        os.environ["REQUESTS_CA_BUNDLE"] = self.ca_path
        os.environ.setdefault("SSL_CERT_FILE", self.ca_path)
        os.environ.setdefault("REQUESTS_CA_BUNDLE", self.ca_path)
        print("ca file found:", shutil.which("cacert"))
        if not os.path.exists(self.ca_path):
            raise FileNotFoundError(f"CA bundle not found: {self.ca_path}")

        #Pathing exes
        self.ytdlp_path = os.path.join(os.path.dirname(__file__), "..", "Util", "yt-dlp.exe")
        self.certificate_path = os.path.join(os.path.dirname(__file__), "..", "Util", "cacert.pem")
        self.cookies_path = os.path.join(os.path.dirname(__file__), "..", "Util", "cookies.txt")
        self.node_path = os.path.join(os.path.dirname(__file__), "..", "Util", "node.exe")
    
    def FormatErrorPrev(self, format):
        # Checks if the users json is correct
        # If not, reverts back to default json
        if self.jsoncontrol["downloader"]["formats"][format] in self.acceptedFormats[format]:
            return self.jsoncontrol["downloader"]["formats"][format]
        else:
            return self.defaultJson["downloader"]["formats"][format]
        
    def detect_playlist(self):
        # Goes through the url to see if it's a playlist
        url = str(self.url)
        index_pos = url.find("index=")
        radio_pos = url.find("radio=")

        start_pos = index_pos if index_pos != -1 else radio_pos

        if start_pos == -1:
            return False

        start_pos += 6  # Length of 'index=' or 'radio='
        index_num = ""

        while start_pos < len(url) and url[start_pos].isdigit():
            index_num += url[start_pos]
            start_pos += 1

        return index_num

    def build_command(self):
        if self.selection == 1:
            # Video Only Command
           command = {
               "format": "bestvideo",
               "verbose": True,
               "postprocessors": [{
                   "key": "FFmpegVideoConvertor",
                   "preferedformat": self.FormatErrorPrev("video"),
               }]
               
           }
           print("Video only")
           
           
        elif self.selection == 2:
            # Audio Only Command
            command = {
               "format": "bestaudio",
               "verbose": True,
               "postprocessors": [{
                   "key": "FFmpegExtractAudio", 
                    "preferredcodec": self.FormatErrorPrev("audio"),
                   "preferredquality": "192",
                   "nopostoverwrites" : False
               }],
               "keepvideo": False
           }
            print("Audio Only")
            
            
        elif self.selection == 3:
            # Both Video & Audio Command
            command = {
               "format": "bestvideo*[vcodec^=avc]+bestaudio/best",
               "verbose": True,
               "postprocessors": [{
                   "key": "FFmpegVideoConvertor", 
                   "preferedformat": self.FormatErrorPrev("video_audio"),
               }],
            }
            print("Video + Audio")
        else:
            return None
        
        #Clipping add
        if self.clipping: 
            command.update({"download_ranges": download_range_func(None, [(self.start, self.end)]),
                            "force_keyframes_at_cuts": True})
            
        #Cookies and etc add
        command["cookiefile"] = self.cookies_path
        command.update({"compat_opts": ["no-certifi"], "nocheckcertificate": True})
        
        
        #Playlist add
        if self.is_playlist and not self.want_playlist_downloaded: command["playlist_items"] = str(self.is_playlist)
        
        #File pathing
        command.update({"paths": {'home': self.file_path}})
        '''
        if self.is_playlist:
            command.extend(
                [
                    "--playlist-items",
                    str(self.is_playlist),
                    "-P",
                    self.file_path,
                    self.url,
                ]
            )
        else:
            command.extend(["-P", self.file_path, self.url])
        '''

        return command

    def download(self, command):
        # 
        try:
            with yt_dlp.YoutubeDL(command) as ydl:
                ydl.download([self.url])
            print("Successfully Installed")
            if self.thread is not None:
                lb.stopLoading()
            return 0
        
        except DownloadError as e:
            print(f"Download failed: {e}")
            if self.thread is not None:
                lb.stopLoading()
            return 2
        
        except ExtractorError as e:
            print(f"Extraction failed: {e}")
            if self.thread is not None:
                lb.stopLoading()
            return 3

    def run(self):
        command = self.build_command()
        if command is None:
            print("No valid selection")
            return 1
        print(command)
        return self.download(command)


def main(url, selection, file_path, thread=None, clipping=False, start=0, end=0):
    downloader = Downloader(url, selection, file_path, thread, clipping, start, end)
    return downloader.run()


if __name__ == "__main__":
    main("https://youtu.be/OQDaSeyKwRA?si=1fHLsyIfIqrg7zT_", 2, "downloads/", clipping=True, start=20, end=40)


