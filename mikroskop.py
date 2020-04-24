import pygame,random,os
from pygame import gfxdraw

dir="/Users/og/niva Dropbox/Otto Geller (ogeller)/Animation/"
WIDTH = 1200
HEIGHT = 800  
SP=40  # Geschwindigkeit
RND=70  # Rand
BG=(202,229,248)  # Hintergrundfarbe
BLACK = 0, 0, 0
TRANSPARENT = 0,0,0,0
SCALE=0.35   # Vergrößerungsfaktor
TT=10  # ticks... je kleiner desto langsamer
MAL=1  # x-mal alle Monster laden

class Monster(pygame.sprite.Sprite):
    def __init__(self,fn):
        super().__init__()
        print(fn)
        self.name=fn.split('/')[-1]
        image=pygame.image.load(fn).convert()
        _,_,b,h=image.get_rect()
        b=int(SCALE*b)
        h=int(SCALE*h)
        self.image=pygame.transform.scale(image,(b,h))
        self.b=b
        self.h=h
        x0=random.randint(0,WIDTH-b)
        y0=random.randint(0,HEIGHT-h)
        self.rect=self.image.get_rect()
        self.rect.x=x0
        self.rect.y=y0
        self.vx=random.randint(-SP,SP)
        self.vy=random.randint(-SP,SP)

    def update(self):
        self.rect.x+=self.vx
        self.rect.y+=self.vy
        #pygame.transform.rotate(self.image,random.randint(-45,45))
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
        x,y,b,h=self.rect
        if x+b>WIDTH:
            self.vx=-self.vx
            self.rect.x=WIDTH-b
        elif x<0:
            self.vx=-self.vx
            self.rect.x=0
        else:
            self.vx=random.randint(-SP,SP)
            self.vy=random.randint(-SP,SP)
        if y+h>HEIGHT:
            self.vy=-self.vy
            self.rect.y=HEIGHT-h
        elif y<0:
            self.vy=-self.vy
            self.rect.y=0
        else:
            self.vx=random.randint(-SP,SP)
            self.vy=random.randint(-SP,SP)
        #self.image=pygame.transform.rotate(self.image,random.randint(-180,180))
        #rect1=self.image.get_rect()
        #self.image.blit(self.image,(x-rect1.center[0],y-rect1.center[1]))

pygame.init()

win = pygame.display.set_mode((WIDTH,HEIGHT))
top=win.copy().convert_alpha()

pygame.display.set_caption("Mikroskop")

mliste=pygame.sprite.Group()


# alle Dateien mit Monstern suchen und Monster initialisierten
fliste=[]
for root, dirs, files in os.walk('./die_bösen/'):
    for name in files:
        print(name)
        if name[0]=='x' and name.split('.')[-1]=='png':
            fliste.append(os.path.join(root,name))
print(fliste)
for f in fliste:
    for i in range(MAL):
        m=Monster(dir+f)
        mliste.add(m)
        #alle_sprites.add(m)


clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, 16, 2, 4096)
ouch = pygame.mixer.Sound("sinus0komma1s.wav")

def redrawGameWindow():
    global frame,TT
    win.fill(BG)  # Hintergrundfarbe
    top.fill(BLACK)
    #win.blit(oben.image,oben.rect)
    # alle Monster
    for el in mliste:
        #scale=random.randint(3,6)/4
        #bild=pygame.transform.scale(el.image,(int(el.b*scale),int(el.h*scale)))
        #bild=pygame.transform.rotate(bild,random.randint(-90,90))
        bild=pygame.transform.rotate(el.image,random.randint(-180,180))
        #rect1=bild.get_rect()
        x,y,_,_=el.rect
        win.blit(bild,(x,y)) #(x-rect1.center[0],y-rect1.center[1]))
        pass
    
    # transparenten Kreis in top malen
    pygame.gfxdraw.filled_circle(top, (WIDTH)//2, HEIGHT//2, int(HEIGHT*0.88/2), TRANSPARENT)
    win.blit(top,(0,0))

    pygame.display.flip() #update() 

    # Frame speichern
    pygame.image.save(win,f'{dir}videoframes-tt{TT}-scale{int(SCALE*100)}/m{frame:04}.png')
    frame+=1

    # alle Monster weiterbewegen
    mliste.update()


run = True
frame=0

while run:
    # je kleiner tick, desto langsamer
    clock.tick(TT)
    if frame>1000:
        run = False
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