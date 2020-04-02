import pygame
pygame.init()

ScrWidth=800
ScrHeight=600

win=pygame.display.set_mode((ScrWidth,ScrHeight))

pygame.display.set_caption("Corona Killer 2d")

walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('level_airport.png')
char = pygame.image.load('standing.png')
drop=pygame.image.load('bullet.png')

clock=pygame.time.Clock()

class player(object):
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=5
        self.isJump=False
        self.jumpCount=10
        self.left=False
        self.right=False
        self.walkCount=0
        self.standing=True
        
    def draw(self,win):
        if self.walkCount+1>=27:
            self.walkCount=0
        if not(self.standing):      
            if self.left:
                win.blit(walkLeft[self.walkCount//3],(int(self.x),int(self.y)))
                self.walkCount+=1
            elif self.right:
                win.blit(pygame.transform.flip(walkLeft[self.walkCount//3],True,False),(int(self.x),int(self.y)))
                self.walkCount+=1
        else:
            if self.right:
                win.blit(pygame.transform.flip(walkLeft[0],True,False),(int(self.x),int(self.y)))
            else:
                win.blit(walkLeft[0],(int(self.x),int(self.y)))

class projectile(object):
    def __init__(self,x,y,facing):
        self.x=x
        self.y=y
        self.width=15
        self.height=15
        self.facing=facing
        self.vel=8*facing 
        
    
    def draw(self,win):
        win.blit(drop,(self.x,self.y))

class enemy(object):
    walkRight=[pygame.image.load('E1.png'),pygame.image.load('E2.png'),pygame.image.load('E3.png'),pygame.image.load('E4.png'),pygame.image.load('E5.png'),pygame.image.load('E6.png'),pygame.image.load('E7.png'),pygame.image.load('E8.png'),pygame.image.load('E9.png')]
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.path=[self.x,self.end]
        self.walkCount=0
        self.vel=3
        
    def draw(self,win):
        self.move()
        if self.walkCount+1>=27:
            self.walkCount=0
        if self.vel>0:
            win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
            self.walkCount+=1
        else:
            win.blit(pygame.transform.flip(self.walkRight[self.walkCount//3],True,False),(self.x,self.y))
            self.walkCount+=1
        
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
               
            
        
def redrawGameWindow():
    win.blit(bg,(0,0)) 
    Vovchik.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    corona.draw(win)
    
    
    
    pygame.display.update()

#mainloop
Vovchik=player(336,536,64,64)
corona=enemy(100,410,64,64,450)
bullets=[]
run = True
while run:
    clock.tick(27)
 #bullets
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
 
    for bullet in bullets:
        if bullet.x<800 and bullet.x>0:
            bullet.x-=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
 #Input  
    keys=pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        if Vovchik.left:
            facing=1
        else:
            facing=-1
        
        if len(bullets)<5:
            bullets.append(projectile(round(Vovchik.x+Vovchik.width//2),round(Vovchik.y+Vovchik.height//2),facing))
 
    if keys[pygame.K_LEFT] and Vovchik.x>Vovchik.vel:
        Vovchik.x-=Vovchik.vel
        Vovchik.left=True
        Vovchik.right=False
        Vovchik.standing=False
    elif keys[pygame.K_RIGHT] and Vovchik.x<ScrWidth-Vovchik.width-Vovchik.vel:
        Vovchik.x+=Vovchik.vel
        Vovchik.right=True
        Vovchik.left=False
        Vovchik.standing=False
    else:
        Vovchik.standing=True
        Vovchik.walkCount=0
    if not(Vovchik.isJump):
        if keys[pygame.K_UP]:
            Vovchik.isJump=True
            Vovchik.right=False
            Vovchik.left=False
            Vovchik.walkCount=0
    else:
        if Vovchik.jumpCount>=-10:
            neg=1
            if Vovchik.jumpCount<0:
                neg=-1
            Vovchik.y-=(Vovchik.jumpCount**2)*0.5*neg
            Vovchik.jumpCount-=1
        else:
            Vovchik.isJump=False
            Vovchik.jumpCount=10     

    redrawGameWindow()
pygame.quit()