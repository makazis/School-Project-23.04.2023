import pygame
from time import *
pygame.init()
win=pygame.display.set_mode((300,300))
sleep(5)
pygame.mixer.music.load("1.mp3")
pygame.mixer.music.play(0,0,800)
run=True
click=[0,0,0]
def check_events():
    global run,keys,mouse_pos,mouse_down,click
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    keys=pygame.key.get_pressed()
    if keys[27]: run=False
    mouse_pos=pygame.mouse.get_pos()
    mouse_down=pygame.mouse.get_pressed()
    for i in range(3):
        if mouse_down[i]:
            click[i]+=1
        else:
            click[i]=0
clicks=[]
start_time=time()
while run:
    check_events()
    if click[0]==1:
        clicks.append(time()-start_time)
        
