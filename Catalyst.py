from math import *
from random import *
import pygame
from Player import *
#from NPCs import *
from time import *
pygame.init()
win=pygame.display.set_mode((0,0))
winsize=win.get_size()
S=pygame.Surface((1800,900))
S2=pygame.Surface((1800,900))
S2.set_colorkey((0,0,4))
Mbonus=[winsize[0]/1800,winsize[1]/900]
run=True
pygame.mouse.set_visible(False)
Level_banner=[pygame.transform.scale(Ssheet.subsurface(0,30+i*50,300,50),(1800,300)) for i in range(10)]
Song_offset=[0.2,1,1]
Graveyard_S=pygame.transform.scale(Ssheet.subsurface((330,80,30,30)),(300,300))
Graveyard_S2=pygame.Surface((1800,900))
Graveyard_S2.fill((0,225,155))
Graveyard_S2.set_alpha(0)
"""
Levels are as follows:
1. Cheetahmen (Action 52)
Name: Mayhem
Difficulty: 4/10
BPM=150

2. Fantasie imprmptu(meganeko remix)
Name: Graveyard
Difficulty: 8/10
BPM=400

3. CCremix
Name: The Funny
Difficulty: 10/10

4. Es nevaru but balts, Kudo nor hardstyle remix
Silverish, metallic theme, with a lot of very futuristic, androidic elements
Name: Silverica
Difficulty: 1/10

5. The massacre(FantomenK)
Difficulty: 3/10

6. Code red(Dr phonics)
Difficulty: 7/10

7. oh_the_sonorous(GDMIX)
Difficulty: 6/10

8. Century ways
Difficulty: 9/10

9. counting landscapes
Difficulty: 2/10

10. eigto x immortals
Difficulty: 5/10

BOSS: Mandragora
BOSS: Enroarching Dark
BOSS: The Hallucination
"""
click=[0,0,0]
def check_events():
    global run,keys,mouse_pos,mouse_down,click
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    keys=pygame.key.get_pressed()
    if keys[27]: run=False
    mouse_pos=pygame.mouse.get_pos()
    mouse_pos=[mouse_pos[i]/Mbonus[i] for i in range(2)]
    mouse_down=pygame.mouse.get_pressed()
    for i in range(3):
        if mouse_down[i]:
            click[i]+=1
        else:
            click[i]=0
slevel=0
menu=1
level=6
level_choice=[0,0,0]
p=Player()
b_in=0
enemies=[]
projectiles=[]
while run:
    check_events()
    S.fill((0,0,0))
    if menu==1: # choose level
        if level_choice==[0,0,0]: # chooses 3 random levels
            level_choice=[]
            ltcf=[0,1,2]
            level_choice=[choice(ltcf)]
            ltcf.remove(level_choice[0])
            level_choice.append(choice(ltcf))
            ltcf.remove(level_choice[1])
            level_choice.append(choice(ltcf))
            ltcf.remove(level_choice[2])
        for i in range(3): # each level entrance is 1800x300, or 300x50
            S.blit(Level_banner[level_choice[i]],(0,i*300))
            if 300+i*300>mouse_pos[1]>i*300:
                if b_in!=i:
                    b_in=i
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Music\\"+str(level_choice[i]+1)+".mp3")
                    pygame.mixer.music.play(99,Song_offset[level_choice[i]],800)
                if click[0]==1:
                    menu=0 #initialize fight
                    slevel=level_choice[i]
                    p.setup()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Music\\"+str(slevel+1)+".mp3")
                    pygame.mixer.music.play(0,Song_offset[slevel],800)
                    start_time=time()
                    song_phase=0
                    beat_pulse=0
                    beat_listener=0
                    level_choice=[0,0,0]
                    if slevel==0: enemies=[Entity(0,0) for i in range(4+level)]
                    elif slevel==1:
                        enemies=[Entity(1,0) for i in range(3+level)]
                        enemies.append(Entity(1,1,level))
                        for i in range(level):
                            enemies.append(Entity(1,3,level))
                        S.set_colorkey((0,0,0))
                        for i in range(randint(2,4)):
                            enemies.append(Entity(1,2))
    elif menu==0: # fight mode
        if slevel==0:
            tpassed=time()-start_time
            pbl=beat_listener
            beat_listener=round(round(tpassed,2)%0.8,2)
            if beat_listener<pbl:
                song_phase+=1
                beat_pulse=11
                if 48>song_phase>16:
                    for i in range(max(1,int(level/2))):
                        if randint(1,5)==1:
                            enemies.append(Entity(0,0))
                elif level>0:
                    for i in range(max(1,int(level/2))):
                        if randint(1,30)==1:
                            enemies.append(Entity(0,0))
                if song_phase==46:
                    for i in range(randint(1,level+2)):
                        enemies.append(Entity(0,1))
                if song_phase%8==0:
                    for i in enemies:
                        if i.tips==1:
                            i.activated=True
                if level>2:
                    if 48>song_phase>32:
                        for i in range(randint(0,max(1,int(level/2)))):
                            if randint(1,5)==1:
                                enemies.append(Entity(0,2))
            if beat_pulse>0:
                beat_pulse-=1
            S.fill((12+beat_pulse*3,12+beat_pulse*3,0))
            S2.fill((0,0,4))
            Pmask=pygame.mask.from_surface(p.sprite)
            for i in enemies:
                if i.tips==1:
                    if i.activated:
                        pygame.draw.line(S2,(180,161,0),(i.x,i.y),(i.x-cos(i.angle)*2700,i.y-sin(i.angle)*2700),10)
                        pygame.draw.line(S2,(255,228,0),(i.x,i.y),(i.x-cos(i.angle)*2700,i.y-sin(i.angle)*2700),6)
            S2_mask=pygame.mask.from_surface(S2)
            if Pmask.overlap(S2_mask,(-p.x,-p.y)):
                p.hp-=1
            S.blit(S2,(0,0))
            for i in enemies:
                i.exist(song_phase,p,projectiles,enemies)
                esprite=pygame.transform.rotate(i.sprite,90-i.angle/pi*180)
                esprite.set_colorkey(i.sprite.get_colorkey())
                S.blit(esprite,(i.x-esprite.get_width()/2,i.y-esprite.get_height()/2))
            for i in projectiles:
                i.exist(projectiles)
                esprite=pygame.transform.rotate(i.sprite,270-i.angle/pi*180)
                esprite.set_colorkey(i.sprite.get_colorkey())
                S.blit(esprite,(i.x-esprite.get_width()/2,i.y-esprite.get_height()/2))
                if i.level==0 and i.tips==0:
                    Bmask=pygame.mask.from_surface(esprite)
                    if Bmask.overlap(Pmask,(i.x-p.x,i.y-p.y)):
                        p.hp-=10
                        i.despawn(projectiles)
            if p.hp<=0:
                run=False
                print("Skill Issue")
                pass
            else:
                pygame.draw.rect(S,(255-(p.hp/100*255),(p.hp/100*255),0),(0,0,20,p.hp))
            p.exist(keys,mouse_down,mouse_pos,click,enemies,projectiles)
            psprite=pygame.transform.rotate(p.sprite,90-p.angle/pi*180)
            S.blit(psprite,(p.x-psprite.get_width()/2,p.y-psprite.get_height()/2))
            if tpassed>133:
                level+=1
                p.cores[0]+=level
                menu=1
                enemies=[]
                projectiles=[]


                
        if slevel==1:
            S.fill((0,0,0))
            S2.fill((0,0,0))
            tpassed=time()-start_time
            pbl=beat_listener
            beat_listener=round(round(tpassed,2)%0.6,2)
            Pmask=pygame.mask.from_surface(p.sprite)
            if beat_listener<pbl:
                song_phase+=1
                beat_pulse=5
            for i in enemies:
                i.exist(song_phase,p,projectiles,enemies)
                if i.tips==1:
                    for i1 in range(30*level+30):
                        esprite=pygame.transform.rotate(i.sprite,90-i.memory[i1*4][2]/pi*180)
                        esprite.set_colorkey(i.sprite.get_colorkey())
                        S.blit(esprite,(i.memory[i1*4][0]-esprite.get_width()/2,i.memory[i1*4][1]-esprite.get_height()/2))
                        if sqrt((i.memory[i1*4][1]-p.y)**2+(i.memory[i1*4][0]-p.x)**2)<25:
                            p.hp-=1
                else:
                    esprite=pygame.transform.rotate(i.sprite,90-i.angle/pi*180)
                    esprite.set_colorkey(i.sprite.get_colorkey())
                    S.blit(esprite,(i.x-esprite.get_width()/2,i.y-esprite.get_height()/2))
                    if i.tips==3:
                        Bmask=pygame.mask.from_surface(esprite)
                        if Bmask.overlap(Pmask,(i.x-p.x,i.y-p.y)):
                            p.hp-=2
            for i in projectiles:
                i.exist(projectiles)
                esprite=pygame.transform.rotate(i.sprite,270-i.angle/pi*180)
                esprite.set_colorkey(i.sprite.get_colorkey())
                S.blit(esprite,(i.x-esprite.get_width()/2,i.y-esprite.get_height()/2))
                Bmask=pygame.mask.from_surface(esprite)
                if Bmask.overlap(Pmask,(i.x-p.x,i.y-p.y)):
                    if i.tips==0:
                        p.hp-=5
                        i.despawn(projectiles)
            p.exist(keys,mouse_down,mouse_pos,click,enemies,projectiles)
            p.xspeed*=0.98
            p.yspeed*=0.98 #slowig dow for extra fun
            psprite=pygame.transform.rotate(p.sprite,90-p.angle/pi*180)
            S.blit(psprite,(p.x-psprite.get_width()/2,p.y-psprite.get_height()/2))
            S2.blit(S.subsurface((min(max(p.x-150,0),1500),min(max(p.y-150,0),600),300,300)),(min(max(p.x-150,0),1500),min(max(p.y-150,0),600)))
            pygame.draw.rect(S2,(0,0,0),(p.x-300,p.y-300,150,600))
            pygame.draw.rect(S2,(0,0,0),(p.x-300,p.y-300,600,150))
            pygame.draw.rect(S2,(0,0,0),(p.x+150,p.y-300,150,600))
            pygame.draw.rect(S2,(0,0,0),(p.x-300,p.y+150,600,150))
            S2.blit(Graveyard_S,(p.x-150,p.y-150))
            pygame.draw.circle(S2,(255,255,255),(mouse_pos[0],mouse_pos[1]),5)
            if p.hp<=0:
                run=False
                print("Skill Issue")
                pass
            else:
                pygame.draw.rect(S2,(255-(p.hp/100*255),(p.hp/100*255),0),(0,0,20,p.hp))
            if beat_pulse>0:
                Graveyard_S2.set_alpha(beat_pulse*10)
                S2.blit(Graveyard_S2,(0,0))
                beat_pulse-=1
            if tpassed>183:
                level+=1
                p.cores[1]+=level
                menu=1
                enemies=[]
                projectiles=[]
    pygame.draw.circle(S,(255,255,255),(mouse_pos[0],mouse_pos[1]),5)
    if slevel==1 and menu==0:
        win.blit(pygame.transform.scale(S2,winsize),(0,0))
    else:
        win.blit(pygame.transform.scale(S,winsize),(0,0))
    pygame.display.update()
pygame.quit()


