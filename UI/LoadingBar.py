import json
import os
import re
from os.path import isfile, join
import sys
import pygame
from BackEnd import file_utils 

running = True

def load_frame_paths(sprite_folder):
    folder = file_utils.resource_path(sprite_folder)
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"Sprite folder not found: {folder}")

    pattern = re.compile(r'Loading-(\d+)\.\w+$') 
    numbered = []
    for name in os.listdir(folder):
        full = join(folder, name)
        if not isfile(full):
            continue
        m = pattern.match(name)
        if m:
            numbered.append((int(m.group(1)), name))

    if not numbered:
        files = [f for f in os.listdir(folder) if isfile(join(folder, f))]
        files.sort()
        return [join(folder, f) for f in files]

    numbered.sort(key=lambda t: t[0])
    return [join(folder, name) for (_, name) in numbered]


def stopLoading():
    global running
    running = False

def defaultSprite(sprite):
    json_path = file_utils.resource_path("Util/user-experience.json")
    with open(json_path, 'r') as file:
        jsoncontrol = json.load(file)
        
    jsoncontrol["loading_bar"]["loaded_sprite"] = sprite
    
    file_utils.atomic_write_json(json_path, jsoncontrol)
    
    return jsoncontrol

def main(x, y, sprite="CharlieBrownGif", fps=60, debug=False):
    global running
    running = True
    sprite_folder = f"Util/Sprite/LoadingSprite/{sprite}"
    
    jsoncontrol = defaultSprite(sprite)

    
    frame_paths = load_frame_paths(sprite_folder)
    total_frames = len(frame_paths)
    if total_frames == 0:
        raise RuntimeError(f"No frames found in {sprite_folder}")

    ticks_per_frame = max(1, fps // total_frames)

    if debug:
        print("DEBUG: sprite_folder =", file_utils.resource_path(sprite_folder))
        print("DEBUG: total_frames =", total_frames)
        print("DEBUG: ticks_per_frame =", ticks_per_frame)
        print("DEBUG: loop duration seconds =", (total_frames * ticks_per_frame) / fps)

    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
    screen = pygame.display.set_mode((400, 300))
    clock = pygame.time.Clock()

    fontfilepath = file_utils.resource_path("Util/Font/DTM-Sans.ttf")
    font = pygame.font.Font(fontfilepath, 50)

    bkrectwidth, bkrectheight = 300, 25
    bkrect_dim = bkBar(bkrectwidth, bkrectheight, screen)
    LdRect_dim = [bkrect_dim[0], bkrect_dim[1], bkrect_dim[2] - 250, bkrect_dim[3]]


    tick = 0  

        
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        frame_index = (tick // ticks_per_frame) % total_frames
        sprite_path = frame_paths[frame_index]
        sprite_surf = pygame.image.load(sprite_path)

        screen.fill(jsoncontrol["loading_bar"]["background_color"])
        sprite_surf = pygame.transform.scale(sprite_surf, (200, 200))
        screen.blit(sprite_surf, (200 - sprite_surf.get_width() // 2, 150 - sprite_surf.get_height() // 2))

        LoadingTxt = font.render("Loading...", True, jsoncontrol["loading_bar"]["font_color"])
        screen.blit(LoadingTxt, (210 - LoadingTxt.get_width() // 2, 45 - LoadingTxt.get_height() // 2))

        pygame.draw.rect(screen, jsoncontrol["loading_bar"]["backgoundbar_color"], pygame.Rect(bkrect_dim))
        pygame.draw.rect(screen, jsoncontrol["loading_bar"]["movingbar_color"], LdRect_dim)

        LdBarSlide(LdRect_dim)

        tick += 1
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()

def bkBar(rect_width, rect_height, screen):
    screen_width, screen_height = screen.get_size()
    x = (screen_width - rect_width) // 2
    y = (screen_height - rect_height) // 1.1
    return [x, y, rect_width, rect_height]

def LdBarSlide(LdRect_dim):
    if LdRect_dim[0] >= 300 and LdRect_dim[2] != 0:
        LdRect_dim[0] += 2
        LdRect_dim[2] -= 2
    elif LdRect_dim[2] != 50:
        LdRect_dim[0] = 50
        LdRect_dim[2] += 2
    else:
        LdRect_dim[0] += 2

if __name__ == "__main__":
    main(200, 100, sprite="Sonic Shadow Dap", debug=True)
