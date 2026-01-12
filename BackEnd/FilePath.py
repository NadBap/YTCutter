import os
from UI.LoadingBar import resource_path as rp

folder = rp("Util/Sprite/LoadingSprite/CharlieBrownGif")
listdir = os.listdir(folder)

for i, filename in enumerate(listdir, start=1):
    old_path = os.path.join(folder, filename)
    new_path = os.path.join(folder, f"Loading-{i}.gif")
    print("Renaming:", old_path, "→", new_path)
    os.rename(old_path, new_path)