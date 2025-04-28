import subprocess

command = ["yt-dlp", "--get-title", "https://www.youtube.com/watch?v=eeKRqnNHIAg"]
ello = subprocess.run(command, check=True, text=True, capture_output=True)
print(ello.stdout.strip())