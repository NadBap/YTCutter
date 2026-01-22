import os
from BackEnd.file_utils import resource_path as rp

folder = rp("Util/Sprite/LoadingSprite/Dante Dancing DMC")
listdir = os.listdir(folder)

for i, filename in enumerate(listdir, start=1):
    old_path = os.path.join(folder, filename)
    new_path = os.path.join(folder, f"Loading-{i}.gif")
    print("Renaming:", old_path, " to ", new_path)
    os.rename(old_path, new_path)