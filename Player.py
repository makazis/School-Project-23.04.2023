from random import *
from math import *
import pygame
Ssheet=pygame.image.load("Sprites.xcf")
class Player:
    def __init__(self):
        self.cores=[0 for i in range(10)]
        self.level=0 
        self.sprite=pygame.Surface((20,20))
        self.sprite.set_colorkey((0,0,0))
        self.dash_reload=0
        self.invincibility=0
        self.mouse_down=[False,False,False]
        self.resprite()
    def resprite(self):
        self.sprite.fill((0,0,0))
        if not self.mouse_down[0]: pygame.draw.circle(self.sprite,(55,55,55),(10,10),10)
        else: pygame.draw.circle(self.sprite,(155,155,155),(10,10),10)
        if self.dash_reload==0: pygame.draw.circle(self.sprite,(255,255,255),(10,10),8)
        else: pygame.draw.circle(self.sprite,(0,0,0),(10,10),8)
        pygame.draw.circle(self.sprite,(0,0,0),(10,10),6)
        pygame.draw.rect(self.sprite,(0,0,0),(7,0,6,20))
        if self.invincibility>0: pygame.draw.circle(self.sprite,(180,161,0),(10,10),4)
        else: pygame.draw.circle(self.sprite,(155,155,155),(10,10),4)
    def setup(self):
        self.dash_reload=0
        self.invincibility=0
        self.invincihp=0
        self.angle=0
        self.x=900
        self.y=450
        self.xspeed=0
        self.yspeed=0
        self.hp=100
        self.vectors=[]
    def exist(self,keys,mouse_down,mouse_pos,click,enemies):
        self.mouse_down=mouse_down
        self.resprite()
        self.angle=atan2(mouse_pos[1]-self.y,mouse_pos[0]-self.x)
        if mouse_down[0]:
            self.vectors.append([cos(self.angle)/16,sin(self.angle)/16])
        if self.dash_reload==0 and click[2]==1:
            self.dash_reload=400
            dash_power=5+0.3*self.cores[0]
            self.vectors.append([cos(self.angle+randint(-300,300)/1000)*dash_power,sin(self.angle+randint(-300,300)/1000)*dash_power])
            if self.cores[0]>0:
                self.invincibility+=self.cores[0]*10
                self.invincihp=self.hp
        elif self.dash_reload>0:
            self.dash_reload-=1
        if self.invincibility>0:
            self.invincibility-=1
            self.hp=self.invincihp
            for i in enemies:
                if sqrt((self.x-i.x)**2+(self.y-i.y)**2)<19:
                    if [i.level,i.tips] in [[0,0]]:
                        i.die(enemies)
                    elif [i.level,i.tips] in [[0,1]]:
                        i.activated=False
        for i in self.vectors:
            self.xspeed+=i[0]
            self.yspeed+=i[1]
        self.vectors=[]
        self.xspeed*=0.99
        self.yspeed*=0.99
        if abs(self.xspeed)<0.025:
            self.xspeed=0
        if abs(self.yspeed)<0.025:
            self.yspeed=0
        self.x+=self.xspeed
        self.y+=self.yspeed
        self.x=min(1800,max(0,self.x))
        self.y=min(900,max(0,self.y))
