import json
import os
import subprocess
import shutil
from BackEnd import file_utils 
from UI import LoadingBar as lb


class Downloader:
    def __init__(self, url, selection, file_path, thread=None):
        self.url = url
        self.selection = selection
        self.file_path = file_path
        self.thread = thread
        self.is_playlist = self.detect_playlist()
        self.want_playlist_downloaded = True
        
        json_path = file_utils.resource_path("Util/user-experience.json")
        with open(json_path, 'r') as file:
            self.jsoncontrol = json.load(file)
            
        ffmpeg_path = os.path.join(os.path.dirname(__file__), "..", "Util", "ffmpeg")
        os.environ["PATH"] += os.pathsep + ffmpeg_path
        


        print("ffmpeg found:", shutil.which("ffmpeg"))
        print(f"Selection: {selection}")
        
        self.ca_path = file_utils.resource_path("Util/cacert.pem")
        print(self.ca_path)
        os.environ["SSL_CERT_FILE"] = self.ca_path
        os.environ["REQUESTS_CA_BUNDLE"] = self.ca_path
        os.environ.setdefault("SSL_CERT_FILE", self.ca_path)
        os.environ.setdefault("REQUESTS_CA_BUNDLE", self.ca_path)
        print("ca file found:", shutil.which("cacert"))
        if not os.path.exists(self.ca_path):
            raise FileNotFoundError(f"CA bundle not found: {self.ca_path}")

        self.ytdlp_path = os.path.join(os.path.dirname(__file__), "..", "Util", "yt-dlp.exe")
        # self.certificate_path = os.path.join(os.path.dirname(__file__), "..", "Util", "cacert.pem")
        self.cookies_path = os.path.join(os.path.dirname(__file__), "..", "Util", "cookies.txt")
    def detect_playlist(self):
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
           command = [
                    self.ytdlp_path,
                    "-f", "bestvideo+bestaudio/best",
                    "--merge-output-format", self.jsoncontrol["downloader"]["formats"]["video"],
                    "--recode-video", self.jsoncontrol["downloader"]["formats"]["video"],
                    "--postprocessor-args", "ffmpeg:-c:v libx264 -crf 18 -preset ultrafast -an"
                ]
           print("Video only")
        elif self.selection == 2:
            command = [
                self.ytdlp_path,
        "-f", "bestaudio/best",
        "--extract-audio",
        "--audio-format", self.jsoncontrol["downloader"]["formats"]["audio"],
        "--audio-quality", "0",
            ]
            print("Audio Only")
        elif self.selection == 3:
            command = [
                self.ytdlp_path,
                "-f",
                "bestvideo+bestaudio/best",
                "--merge-output-format", self.jsoncontrol["downloader"]["formats"]["video_audio"],
                "--recode-video", self.jsoncontrol["downloader"]["formats"]["video_audio"],
                "--postprocessor-args", "ffmpeg:-c:v libx264 -crf 18 -preset ultrafast -c:a aac -b:a 192k"
            ]
            print("Video + Audio")
        else:
            return None
        
        command.extend(["--cookies", self.cookies_path])
        if self.is_playlist and not self.want_playlist_downloaded: command.extend(["--playlist-items", str(self.is_playlist)])
        
        command.extend(["-P", self.file_path, self.url])
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
        try:
            subprocess.run(command, check=True, text=True)
            print("Successfully Installed")
            if self.thread is not None:
                lb.stopLoading()
            return 0
        except subprocess.CalledProcessError as e:
            print("An error occurred while downloading")
            print(f"Error Output: {e.returncode} {e}")
            if self.thread is not None:
                lb.stopLoading()
            return 2

    def run(self):
        command = self.build_command()
        if command is None:
            print("No valid selection")
            return 1
        return self.download(command)


def main(url, selection, file_path, thread=None):
    downloader = Downloader(url, selection, file_path, thread)
    return downloader.run()


if __name__ == "__main__":
    main("https://www.youtube.com/watch?v=IbYAVBp4KRE", 3, "downloads/")
