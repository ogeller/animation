import numpy as np
import cv2
import time

BG=(202,229,248)  # Hintergrundfarbe

dir="/Users/og/niva Dropbox/Otto Geller (ogeller)/Animation/"

cv2.namedWindow('Otto', cv2.WINDOW_NORMAL)

im=cv2.imread(dir+'blaue teile 4.png')#, cv2.IMREAD_COLOR)
print('im: ',im.shape,im.size)

height, width = im.shape[:2]
#im1=cv2.resize(im,(width//4,height//4))
im1=im
print('im1: ',im1.shape,im1.size)

imgray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
erg = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
if len(erg)==2:
    contours, hierarchy=erg
else:
    _,contours, hierarchy=erg
#img = cv2.drawContours(im, contours, -1, (0,255,0), 2)
#print(contours)
ebene1=[]
next1=hierarchy[0][0][2]
fertig=False
for i,c in enumerate(hierarchy[0]):
    #print(i,c)
    if fertig:
        break
    elif i==next1:
        ebene1.append(i)
        next1=c[0]
        #print('next1=',next1)
        if next1==-1:
            fertig=True
    else:
        pass
print(ebene1)

for i,x in enumerate(ebene1):
    x,y,w,h=cv2.boundingRect(contours[x])
    figur=im1[y:y+h,x:x+w]
    print('figur: ',i,' - x,y,w,h=',x,y,w,h,'shape=',figur.shape,'size=',figur.size)
    cv2.imshow(str(i),figur)
    cv2.imwrite(dir+'/out/x'+str(i)+'.png',figur)

    #img=cv2.rectangle(im1,(x,y),(x+w,y+h),(0,0,0),1)
cv2.imshow('Otto',im1)
    #time.sleep(1)


k=cv2.waitKey(0) & 0xFF
if k==ord('k'):
    cv2.destroyAllWindows()


