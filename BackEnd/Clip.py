import subprocess
from UI import LoadingBar as lb
from BackEnd import Downloader as DDD

class Clip(DDD.Downloader):
    def __init__(self, url, selection, file_path, start, end, thread=None):
        self.start = start
        self.end = end
        super().__init__(url, selection, file_path, thread)
    
def build_command(self, start, end):
    command = ["yt-dlp", "--download-sections", f"*{start}-{end}"]
    if self.selection == 1:
        command.extend([
            "-f", "bestvideo[ext=mp4]"
        ])
    elif self.selection == 2:
        command.extend([
            "-f", "bestaudio",
            "--extract-audio", "--audio-format", "mp3"
        ])
    elif self.selection == 3:
        command.extend([
            "-f", "best[ext=mp4]",
            "--merge-output-format", "mp4"
        ])
    else:
        return None
    
    if self.is_playlist:
        command.extend([
            "--playlist-items", str(self.is_playlist),
            self.url,
            "-P", self.file_path
        ])
    else:
        command.extend([
            self.url,
            "-P", self.file_path
        ])

    
    def run(self):
        command = self.build_command(self.start, self.end)
        if command is None:
            print("No valid selection")
            return 1
        self.download(command)
        
def main(url, selection, file_path, start, end, thread=None):
    clip = Clip(url, selection, file_path, start, end, thread)
    return clip.run()