from math import *
from random import *
import pygame
Ssheet=pygame.image.load("Sprites.xcf")
class Entity:
    def __init__(self,level,tips,difficulty=0):
        self.difficulty=0
        self.level=level
        self.tips=tips
        self.pb=0
        self.vectors=[]
        self.xspeed=0
        self.yspeed=0
        self.alive=True
        self.angle=0
        self.AI=[]
        self.x=900
        self.y=450
        self.xspeed=0
        self.yspeed=0
        if self.level==0:
            if self.tips==0: # Warning Landmines, release bullets every big beat, if not shot
                if randint(1,2)==1:
                    self.y=randint(0,1)*900
                    self.x=randint(30,1740)
                    self.yspeed=(1-self.y/450)*randint(10,50)/10
                else:
                    self.y=randint(30,840)
                    self.x=randint(0,1)*1800
                    self.xspeed=(1-self.x/900)*randint(10,100)/10
                self.sprite=Ssheet.subsurface((301,31,18,18))
            elif self.tips==1: # Warning Single Laser Spinner
                if randint(1,2)==1:
                    self.y=randint(0,1)*900
                    self.x=randint(30,1740)
                    self.yspeed=(1-self.y/450)*randint(10,50)/10
                else:
                    self.y=randint(30,840)
                    self.x=randint(0,1)*1800
                    self.xspeed=(1-self.x/900)*randint(10,100)/10
                self.angle=randint(0,round(2*pi*100))/100
                self.sprite=Ssheet.subsurface((303,53,24,25))
                self.activated=False
                self.AI=[choice(("Slow Spinning Left","Slow Spinning Right"))]
            elif self.tips==2: #ringing mines
                if randint(1,2)==1:
                    self.y=randint(0,1)*900
                    self.x=randint(30,1740)
                    self.yspeed=(1-self.y/450)*randint(10,50)/10
                else:
                    self.y=randint(30,840)
                    self.x=randint(0,1)*1800
                    self.xspeed=(1-self.x/900)*randint(10,100)/10
                self.sprite=Ssheet.subsurface((330,30,18,18))
        elif self.level==1:
            if self.tips==0:
                self.attack_angle=randint(-100,100)/100
                self.x=150
                self.angle=randint(0,round(2*pi*100))/100
                self.xspeed=cos(self.angle)*3
                self.yspeed=sin(self.angle)*3
                self.sprite=Ssheet.subsurface((300,111,7,7))
            elif self.tips==1:
                self.x=150
                self.sprite=Ssheet.subsurface((300,80,30,30))
                self.memory=[[-100,-100,0] for i in range(difficulty*120+220)]
            elif self.tips==2:
                self.x=randint(100,1700)
                self.y=randint(100,800)
                self.sprite=Ssheet.subsurface((312,111,9,9))
            elif self.tips==3:
                self.sprite=pygame.transform.scale(Ssheet.subsurface((312,120,9,9)),(45,45))
                self.new_x=0
                self.new_y=0
                self.y=0
                self.x=0
        self.sprite.set_colorkey((255,255,255))
    def exist(self,bsf,p,projectiles,enemies):
        for i in self.vectors:
            self.xspeed+=i[0]
            self.yspeed+=i[1]
        self.vectors=[]
        self.x+=self.xspeed
        self.y+=self.yspeed
        self.xspeed*=0.99
        self.yspeed*=0.99
        if abs(self.xspeed)<0.025:
            self.xspeed=0
        if abs(self.yspeed)<0.025:
            self.yspeed=0
        self.x=min(1800,max(0,self.x))
        self.y=min(900,max(0,self.y))
        if "Slow Spinning Right" in self.AI: #general AI manipulation
            self.angle+=0.0015
        elif "Slow Spinning Left" in self.AI: #general AI manipulation
            self.angle-=0.0015
        if self.level==0:
            if self.tips==0:
                if self.pb!=bsf:
                    self.pb=bsf
                    if randint(1,3)==1:
                        projectiles.append(Projectile(self,0,0))
                self.angle=atan2(p.y-self.y,p.x-self.x)
            elif self.tips==2:
                if self.pb!=bsf:
                    self.pb=bsf
                    if randint(1,5)==1:
                        self.angle=self.angle=randint(0,round(2*pi*100))/100
                        self.vectors.append([cos(self.angle)*2,sin(self.angle)*2])
                else:
                    for i in enemies:
                        if sqrt((self.x-i.x)**2+(self.y-i.y)**2)<60 and i!=self:
                            angl=atan2(self.y-i.y,self.x-i.x)+pi/4
                            i.vectors.append([cos(angl)/4,sin(angl)/4])
                    for i in projectiles:
                        if sqrt((self.x-i.x)**2+(self.y-i.y)**2)<60:
                            angl=atan2(self.y-i.y,self.x-i.x)+pi/4
                            i.vectors.append([cos(angl)/4,sin(angl)/4])
                    if sqrt((self.x-p.x)**2+(self.y-p.y)**2)<60:
                        angl=atan2(self.y-p.y,self.x-p.x)+pi/4
                        p.vectors.append([cos(angl)/4,sin(angl)/4])
                    self.x=min(1700,max(100,self.x))
                    self.y=min(800,max(100,self.y))
        elif self.level==1:
            if self.tips==1: #Speed Snek
                self.memory.pop(0)
                self.memory.append([p.x,p.y,p.angle])
            elif self.tips==0:
                self.angle=atan2(p.y-self.y,p.x-self.x)
                if self.pb!=bsf:
                    self.pb=bsf
                    self.vectors.append([cos(self.angle+self.attack_angle)*2,sin(self.angle+self.attack_angle)*2])
                    if randint(1,2)==1:
                        projectiles.append(Projectile(self,1,0))
            elif self.tips==2:
                self.angle=atan2(p.y-self.y,p.x-self.x)+randint(-100,100)/100
                if sqrt((self.x-p.x)**2+(self.y-p.y)**2)>300:
                    self.vectors.append([cos(self.angle)/5,sin(self.angle)/5])
                elif self.pb!=bsf:
                    self.pb=bsf
                    for i in projectiles:
                        angl=atan2(i.y-self.y,i.x-self.x)
                        i.vectors.append([-cos(angl),-sin(angl)])
            elif self.tips==3:
                if round(self.x)==round(self.new_x) and round(self.y)==round(self.new_y):
                    self.new_x=randint(0,1800)
                    self.new_y=randint(0,900)
                else:
                    self.new_x+=randint(-3,3)
                    self.new_y+=randint(-3,3)
                    angl=atan2(self.new_y-self.y,self.new_x-self.x)
                    self.vectors.append([cos(angl)/20,sin(angl)/20])
    def die(self,lis):
        if self in lis:
            lis.remove(self)
class Projectile:
    def __init__(self,owner,level,tips):
        self.level=level
        self.tips=tips
        self.owner=owner
        self.x=self.owner.x
        self.y=self.owner.y
        self.angle=self.owner.angle
        self.speed=0
        self.vectors=[]
        if self.level==0:
            if self.tips==0: #Warning Landmine Bullet
                self.speed=2
                self.sprite=Ssheet.subsurface((320,30,7,9))
                self.sprite.set_colorkey((255,255,255))
        elif self.level==1:
            if self.tips==0: # ghast_bomb
                self.speed=2
                self.sprite=Ssheet.subsurface((307,111,5,5))
                self.sprite.set_colorkey((255,255,255))
            elif self.tips==2: #player ghyast bomb
                self.speed=7
                self.sprite=Ssheet.subsurface((307,111,5,5))
                self.sprite.set_colorkey((255,255,255))
                self.bounces=randint(0,2)
        if self.speed>0:
            self.xspeed=cos(self.angle)*self.speed
            self.yspeed=sin(self.angle)*self.speed
    def exist(self,projectile_list):
        for i in self.vectors:
            self.xspeed+=i[0]
            self.yspeed+=i[1]
        self.vectors=[]
        self.x+=self.xspeed
        self.y+=self.yspeed
        if self.tips==2 and self.level==1:
            if self.bounces<6:
                if self.x>=1800 or self.x<=0:
                    self.xspeed=-self.xspeed
                    self.bounces+=1
                if self.y>=900 or self.y<=0:
                    self.yspeed=-self.yspeed
                    self.bounces+=1
        if self.x<-100 or self.x>1900 or self.y<-100 or self.y>1000:
            self.despawn(projectile_list)
    def despawn(self,projectile_list):
        if self in projectile_list:
            projectile_list.remove(self)


        

