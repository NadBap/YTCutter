import subprocess
from UI import LoadingBar as lb


class Downloader:
    def __init__(self, url, selection, file_path, thread=None):
        self.url = url
        self.selection = selection
        self.file_path = file_path
        self.thread = thread
        self.is_playlist = self.detect_playlist()

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
            command = ["yt-dlp", "-f", "bestvideo"]
        elif self.selection == 2:
            command = [
                "yt-dlp",
                "-f",
                "bestaudio",
                "--extract-audio",
                "--audio-format",
                "mp3",
            ]
        elif self.selection == 3:
            command = [
                "yt-dlp",
                "-f",
                "bestvideo[ext=mp4]+bestaudio[ext=m4a]",
                "--merge-output-format",
                "mp4",
                "--remux-video",
                "mp4",
            ]
        else:
            return None

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
            subprocess.run(command, check=True, text=True, capture_output=True)
            print("Successfully Installed")
            if self.thread is not None:
                lb.stopLoading()
        except subprocess.CalledProcessError as e:
            print("An error occurred while downloading")
            print(f"Error Output: {e.returncode} {e}")
            if self.thread is not None:
                lb.stopLoading()

    def run(self):
        command = self.build_command()
        if command is None:
            print("No valid selection")
            return 1
        self.download(command)


def main(url, selection, file_path, thread=None):
    downloader = Downloader(url, selection, file_path, thread)
    return downloader.run()


if __name__ == "__main__":
    main("https://www.youtube.com/watch?v=eeKRqnNHIAg", 1, "downloads/")
