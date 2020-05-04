import pygame,random,os
from pygame import gfxdraw

dir="/Users/og/niva Dropbox/Otto Geller (ogeller)/Animation/fische/"
WIDTH = 1200
HEIGHT = 800  
SP=40  # Geschwindigkeit
RND=70  # Rand
BG=(202,229,248)  # Hintergrundfarbe
BLACK = 0, 0, 0
TRANSPARENT = 0,0,0,0
SCALE=0.35   # Vergrößerungsfaktor
TT=10  # ticks... je kleiner desto langsamer
MAL=10  # x-mal alle Monster laden

class Monster(pygame.sprite.Sprite):
    def __init__(self,monstername,images):
        super().__init__()
        self.name=monstername
        self.images=images
        self.nr=0
        self.len=len(images)
        x0=random.randint(0,WIDTH)
        y0=random.randint(0,HEIGHT)
        #pygame.image.load(fn).convert()
        #
        #b=int(SCALE*b)
        #h=int(SCALE*h)
        self.image=images[0] #pygame.transform.scale(image,(b,h))
        x,y,b,h=self.image.get_rect()
        self.b=b
        self.h=h
        self.rect=pygame.Rect((x,y,b,h))
        self.rect.x=x0
        self.rect.y=y0
        self.vx0=-random.randint(5,15)
        self.vx=self.vx0 #random.randint(-SP,SP)
        self.vy=0 #random.randint(-4,4)

    def update(self):
        #print(self.name,self.nr)
        self.vx=self.vx0+random.randint(-4,4)
        self.vy=random.randint(-7,7)
        self.rect.x+=self.vx
        self.rect.y+=self.vy
        if self.nr<self.len-1:
            self.nr+=1 
        else:
            self.nr=0
        self.image=self.images[self.nr]
        #pygame.transform.rotate(self.image,random.randint(-45,45))
        
        # collision
        '''
        mliste.remove(self)
        hitlist=pygame.sprite.spritecollide(self,mliste,False)
        #print(hitlist)
        for m in hitlist:
            #print('hit: ',m.name,self.name)
            # Bewegung rückgängig machen
            self.rect.x-=self.vx
            self.rect.y-=self.vy
            #ouch.play()
        mliste.add(self)
        '''

        x,y,b,h=self.rect
        #print(self.rect)
        '''
        if x+b>WIDTH:
            #self.vx=-self.vx
            self.rect.x=0
        '''
        if x+b<0:
            #self.vx=-self.vx
            self.rect.x=WIDTH
            self.rect.y=random.randint(0,HEIGHT)
        '''
        else:
            self.vx=random.randint(-SP,SP)
            self.vy=random.randint(-SP,SP)
        '''
        if y+h>HEIGHT:
            #self.vy=-self.vy
            self.rect.y=HEIGHT-h
        elif y<0:
            #self.vy=-self.vy
            self.rect.y=0
        else:
            pass
        #else:
        #    self.vx=random.randint(-SP,SP)
        #    self.vy=random.randint(-SP,SP)
        
        #self.image=pygame.transform.rotate(self.image,random.randint(-180,180))
        #rect1=self.image.get_rect()
        #self.image.blit(self.image,(x-rect1.center[0],y-rect1.center[1]))

pygame.init()

win = pygame.display.set_mode((WIDTH,HEIGHT))
top=win.copy().convert_alpha()

pygame.display.set_caption("Fische")

mliste=pygame.sprite.Group()


# alle Dateien mit Monstern suchen und Monster initialisierten
fliste=[]
for root, dirs, files in os.walk('./fische/'):
    for name in files:
        print(name)
        if name[:4]=='test' and name.split('.')[-1]=='png':
            fliste.append(os.path.join(dir,name))
print(fliste)
images=[]
for f in fliste:
    image=pygame.image.load(f).convert()
    _,_,b,h=image.get_rect()
    image=pygame.transform.scale(image,(int(b*SCALE),int(h*SCALE)))
    images.append(image)
for i in range(MAL):
    m=Monster("Monster"+str(i),images)
    mliste.add(m)


clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, 16, 2, 4096)
ouch = pygame.mixer.Sound("sinus0komma1s.wav")

def redrawGameWindow():
    global frame,TT
    win.fill(BG)  # Hintergrundfarbe
    #top.fill(BLACK)
    
    # alle Monster
    for el in mliste:
        #scale=random.randint(3,6)/4
        #bild=pygame.transform.scale(el.image,(int(el.b*scale),int(el.h*scale)))
        #bild=pygame.transform.rotate(bild,random.randint(-90,90))
        #bild=pygame.transform.rotate(el.image,random.randint(-180,180))
        #rect1=bild.get_rect()
        x,y,_,_=el.rect
        win.blit(el.image,(x,y)) #(x-rect1.center[0],y-rect1.center[1]))
        pass
    
    # transparenten Kreis in top malen
    #pygame.gfxdraw.filled_circle(top, (WIDTH)//2, HEIGHT//2, int(HEIGHT*0.88/2), TRANSPARENT)
    #win.blit(top,(0,0))

    pygame.display.flip() #update() 

    # Frame speichern
    #pygame.image.save(win,f'{dir}videoframes-tt{TT}-scale{int(SCALE*100)}/m{frame:04}.png')
    frame+=1

    # alle Monster weiterbewegen
    mliste.update()


run = True
frame=0

while run:
    # je kleiner tick, desto langsamer
    clock.tick(TT)
    #if frame>1000:
    #    run = False
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            pause=True
            while pause:
                for e1 in pygame.event.get():
                    if e1.type == pygame.MOUSEBUTTONDOWN:
                        x,y=pygame.mouse.get_pos()
                        for m in mliste:
                            if x>m.rect.x and x<m.rect.x+m.b and y>m.rect.y and y<m.rect.y+m.h:
                                print(m.name,m.rect.x,m.b,m.rect.y,m.h,'--',x,y)
                        pause=False
    redrawGameWindow() 
    
    
    
pygame.quit()