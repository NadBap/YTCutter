import os
from os import listdir
from os.path import isfile, join
import pygame
    
running = True
spriteType = "Niko Dance"
def main(x, y):
    global running
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    clock = pygame.time.Clock()

    time = 0
    
    bkrectwidth = 300
    bkrectheight = 25
    
    bkrect_dim = bkBar(bkrectwidth, bkrectheight, screen)
    LdRect_dim = [bkrect_dim[0], bkrect_dim[1], bkrect_dim[2] - 250, bkrect_dim[3]]
    
    screen.fill("Dark Blue")
    
    pygame.display.set_caption("Loading")
    pygame.draw.rect(screen, "light gray", pygame.Rect(bkrect_dim))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = True
            fontfilepath = os.path.join(os.path.dirname(__file__), "..", "Util", "Font", "DTM-Sans.ttf")
            fontfilepath = os.path.abspath(fontfilepath)
            font = pygame.font.Font(fontfilepath, 50)
         
        screen.fill("Dark Blue")   
        
        spritefilepath = os.path.join(os.path.dirname(__file__), "..", "Util", "Sprite", "LoadingSprite", spriteType, f"Loading-{FrameLoad(time)}.gif")
        spritefilepath = os.path.abspath(spritefilepath)
        sprite = pygame.image.load(spritefilepath)
        
        sprite = pygame.transform.scale(sprite, (200, 200))
        screen.blit(sprite, (200 - sprite.get_width() // 2, 150 - sprite.get_height() // 2))

        LoadingTxt = font.render("Loading...", True, "Cyan")
        screen.blit(LoadingTxt, (210 - LoadingTxt.get_width() // 2, 45 - LoadingTxt.get_height() // 2))
        
        pygame.draw.rect(screen, "Royal Blue", pygame.Rect(bkrect_dim))
        pygame.draw.rect(screen, "cyan", LdRect_dim)
        
        LdBarSlide(LdRect_dim)
        if time >= 60:
            time = 0
        else:
            time += 1
        clock.tick(60)
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
'''
def FrameLoad(time):
    if time <= 10:
        return 1
    elif time <= 20:
        return 2
    elif time <= 30:
        return 3
    elif time <= 40:
        return 4
    elif time <= 50:
        return 5
    else:
        return 6
'''
def FrameLoad(time):
    onlyfiles = [f for f in listdir(os.path.join(os.path.dirname(__file__), "..", "Util", "Sprite", "LoadingSprite", spriteType)) if isfile(join(os.path.join(os.path.dirname(__file__), "..", "Util", "Sprite", "LoadingSprite", spriteType), f))]
    count = 1
    while True:
        if time / count <= 60/len(onlyfiles):
            return count
        else:
            count += 1
def stopLoading():
    global running
    running = False
if __name__ == "__main__":
    main(200, 100)  