import subprocess

def main(url, selection):
    IsTheirPlay = Playlist(url)
    commands = ComInfo(url, IsTheirPlay, selection)
    if commands == 1:
        print("No valid selection")
        return 1
    Download(commands)

def Download(command):
    try:
        subprocess.run(command, check=True, text=True, capture_output=True)
        print("Successfully Installed")
    except subprocess.CalledProcessError as e:
        print("An error has occured while downloading")

def ComInfo(url, num, selection):
    command = []
    if selection == 1:
        command = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]"
        , "mp4"
        ]
    elif selection == 2:
        command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3"
        ]
    elif selection == 3:
        command = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio",
        "--merge-output-format", "mp4"
        ]
    else:
        return 1
    
    if num != False:
        command.extend(["--playlist-items",
                          str(num), url])
    else:
        command.append(url)
        
    return command
def Playlist(url):
    i = 0
    word = 0
    indexnum = ""
    if "index=" in url: 
        word = url.find("index=")
    elif "radio=" in url:
        word = url.find("radio=")
    else: 
        return False
    
    while True:
        
        if url[word + 6 + i] >= '0' and url[word + 6 + i] <= '9':
            indexnum = indexnum + url[word + 6 + i]
        else:
            break
        i = i + 1
    return indexnum
    