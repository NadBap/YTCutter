import json
import os
import subprocess
import shutil
import sys
from UI import LoadingBar as lb



def resource_path(relative_path):
    if getattr(sys, 'frozen', False): 
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Downloader:
    def __init__(self, url, selection, file_path, thread=None):
        self.url = url
        self.selection = selection
        self.file_path = file_path
        self.thread = thread
        self.is_playlist = self.detect_playlist()
        json_path = resource_path("Util/user-experience.json")
        with open(json_path, 'r') as file:
            self.jsoncontrol = json.load(file)
        ffmpeg_path = os.path.join(os.path.dirname(__file__), "..", "Util", "ffmpeg")
        os.environ["PATH"] += os.pathsep + ffmpeg_path
        print("ffmpeg found:", shutil.which("ffmpeg"))
        print(f"Selection: {selection}")
        
        self.ytdlp_path = os.path.join(os.path.dirname(__file__), "..", "Util", "yt-dlp.exe")

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
                    "--merge-output-format", self.jsoncontrol["Downloader"]["Formats"]["Video"],
                    "--recode-video", self.jsoncontrol["Downloader"]["Formats"]["Video"],
                    "--postprocessor-args", "ffmpeg:-c:v libx264 -crf 18 -preset ultrafast -an"
                ]
           print("Video only")
        elif self.selection == 2:
            command = [
                self.ytdlp_path,
        "-f", "bestaudio/best",
        "--extract-audio",
        "--audio-format", self.jsoncontrol["Downloader"]["Formats"]["Audio"],
        "--audio-quality", "0",
            ]
            print("Audio Only")
        elif self.selection == 3:
            command = [
                self.ytdlp_path,
                "-f",
                "bestvideo+bestaudio/best",
                "--merge-output-format", self.jsoncontrol["Downloader"]["Formats"]["Video-Audio"],
                "--recode-video", self.jsoncontrol["Downloader"]["Formats"]["Video-Audio"],
                "--postprocessor-args", "ffmpeg:-c:v libx264 -crf 18 -preset ultrafast -c:a aac -b:a 192k"
            ]
            print("Video + Audio")
        else:
            return None
        
        command.extend(["--cookies", self.cookies_path])
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
    main("https://www.youtube.com/watch?v=eeKRqnNHIAg", 1, "downloads/")
