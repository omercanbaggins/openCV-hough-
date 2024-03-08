from math import tan
from re import T
from cv2.gapi import RGB2Gray
from cv2.typing import Range
import numpy as np
import cv2
import matplotlib
import sinif1
import math
import serial



arduino = serial.Serial(port='COM6', baudrate=115200, timeout=.1)

def UzaklikBulSerit(resim):
    "'input = resim bir numpy arrary'"
    "'output = integer type uzaklik'"
    
    uzaklik = 0
    x = len(resim)    #len pythonda uzunluk buluyor normalde c de for loop ile bulurdun burda built-in func var
    for i in range(x):   # i yi uzunluk boyunca iterate et
        if resim[1,i]==1.0: # sadece y de yani column da geziniyoruz cunku yatay ile isimiz var ve böylesi daha performansli  time complexity = O(n) diger turlu O(n kare) olur yavaslar
                            #buradaki örnekte diðer taraflar beyaz czgi siyah bu renk deðiþtirilebilir,
            uzaklik+=1      #uzaklik her siyah olmayan noktada 1 artacak 
        else:
            break
    return uzaklik



re1 = np.ones((10,10))        #sadece test amaçli 10 a 10 luk resim yani array ones dedik arkasi beyaz
cv2.line(re1,(5,0),(5,10),(0,255,0),1)  # x=5,y =0 baþlangic x=5 y=10 bitis noktasi, 0,255,0 siyah rengi temsilen, 1 kalinlik

re2 = np.ones((10,10))
cv2.line(re2,(9,0),(9,10),(0,255,0),1)

#print(UzaklikBulSerit(re2))  yorum satirini kaldirip deneyebilirsiniz ikisinde de uzaklik farkli olacak ayrica kanit amacli print('buraya resim gelecek') yapilabilir her eleman gozukur
#print(UzaklikBulSerit(re1))

    
#print(re1)
#print(re2)

#burada 720 x720 resim uretilir  yine ustte belirtildigi gibi baslangic noktalari 400,0 bitis 400,720    3 kalinliginda
def duzCizgiliResim():
    "'output numpy array yani resim uretilip cizgi cizilmis hali'"
    bosResim = np.ones((720,720))
    cv2.line(bosResim,(400,0),(400,720),(0,255,0),3)
    
    #cv2.line(bosResim,(720,0),(720,720),(0,255,0),3)
    return bosResim
    

a =(400,720)
b =(500,0)

c =(400,720)
d = (700,0)

def EgimBul(img,st1,bt1,st2,bt2):
    cv2.line(img,st1,bt1,(0,255,0),3)
    cv2.line(img,st2,bt2,(0,255,0),3)
    egim = (bt1[0]-bt2[0])/(st1[1]-bt1[1])
    degree= math.atan(egim)
    print(degree)

    

def resimMerkezBul(array):
    return len(array)//2

def edgeleme(resim):
    resimgri = np.copy(resim)
    #resimin yedegi olsun diye copy fonksiyonu resim alir tabii
    griSonuc = cv2.cvtColor(resimgri,cv2.COLOR_RGB2GRAY) # iki input parametresi uygulanacak resim ve dönüstürülecek renk
#.
    #resim2 = np.ones((900,900))

    blurSonuc = cv2.GaussianBlur(griSonuc,(5,5),0)        #hepsi ilk input olarak uygulanan resmi aliyor zaten, sonrasinda esik deðerleri
    edgeSonuc = cv2.Canny(blurSonuc,50,150)
    return edgeSonuc


def ilgiBolgesi(resim):
    yukseklik = resim.shape[0]
    cv2.circle(resim,(900,yukseklik),15,(0,255,0),3)
    poligonlar = np.array([[(400,yukseklik),(1100,yukseklik),(1600,0)]])
    maskeleme = np.zeros_like(resim)
    cv2.fillPoly(maskeleme,poligonlar,255)
    meskResim=cv2.bitwise_and(reEdgeleme,maskeleme)
    return meskResim
    

def cizgileriGoruntule(resim,cizgiler):
    cizgiResmi = np.zeros_like(resim)
    if cizgiler is not None:
        for cizgi in cizgiler:
            x1,y1,x2,y2 = cizgi = cizgi.reshape(4)
            cv2.line(cizgiResmi,(x1,y1),(x2,y2),(255,0,0),5)
            cv2.line(cizgiResmi,(x2,y2),(x2,y1),(255,255,0),5)
            tan = (x2-x1)/(y2-y1) 
            degree = math.atan(tan)
            if frameC%24==0:
                #print(x2-x1)
                #print(y2-y1)
                #print(tan)
                katsayi = 180/math.pi
                x =  int(math.atan(tan)*katsayi)
                b = str(x)
                print(b)
                arduino.write(bytes(b,"utf-8"))
                
                
           
            #print(degree)
            return cizgiResmi
    return cizgiResmi

#print(len((5,4)))

def kusBakis(imgR):
    

    top_left = (210, 211)
    bottom_left = (113, 330)

    top_right = (467, 211)
    bottom_right = (593, 330)



    pts1 = np.float32([top_left, bottom_left, top_right, bottom_right])
    pts2 = np.float32([[0,0], [0,480], [640, 0], [640,480]])
    

    
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    transformed_frame = cv2.warpPerspective(imgR, matrix, (640, 480))
    return transformed_frame


#cv2.imshow("iki",resim2)

cap = cv2.VideoCapture("test1.mp4")
frameC = 0
while(cap.isOpened):
    _,frame=cap.read()
    frame = cv2.resize(frame,(640,480))
    #frame = frame.resize(640,480)
    frameC+=1
    
    #resim = cv2.imread("ab.jpg")
    #resimKopya = np.copy(frame)

    #res3 = np.ones((720,720))

    #ornek = np.ones((10,10))
    #cv2.imshow("ornek1",ornek)

    a = kusBakis(frame)
    reEdgeleme = edgeleme(a)
    #kesikResim = ilgiBolgesi(a)
    
    #    cizgiler =cv2.HoughLinesP(kesikResim,2,np.pi/180,100,np.array([]),minLineLength=20,maxLineGap=10)


    cizgiler =cv2.HoughLinesP(reEdgeleme,2,np.pi/180,100,np.array([]),minLineLength=10,maxLineGap=5)
    cv2.imshow("A",a)
    cv2.imshow("red",reEdgeleme)

    cv2.imshow("normal",frame)
 
   
    #combo= cv2.addWeighted(frame,0.8,cizgileriGoruntule(frame,cizgiler),1,1)
    cv2.imshow("final",cizgileriGoruntule(frame,cizgiler))
    cv2.waitKey(1)

