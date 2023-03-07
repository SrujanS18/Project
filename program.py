import cv2
import numpy as np
import matplotlib.pyplot as plt

from picamera import PiCamera

from time import sleep
import time
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
cnlist=[]
totaldist=1000

def capture():
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt

    from picamera import PiCamera

    from time import sleep
    import time
    camera = PiCamera()
    camera.start_preview()
    camera.resolution = (640,480)
    time.sleep (1)
    camera.start_preview()
    camera.capture("hi.jpeg")
    time.sleep(1)
    camera.stop_preview()
    time.sleep(1)
    camera.close()
    
def contour():
    img2 = cv2.imread("/home/pi/Desktop/hi.jpeg")
    img3 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
    img_h2 = cv2.cvtColor(img3, cv2.COLOR_RGB2HSV)
    lower = np.array([35,50,50])
    upper = np.array([82,255,255])
    mask1 = cv2.inRange(img_h2,lower,upper)
    res2 = cv2.bitwise_and(img2,img2,mask=mask1)
    cont,_ = cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    cnlist=[]
    for cnt in cont:
        if(len(cnt)>100):
            x,y,w,h=cv2.boundingRect(cnt)
            cv2.rectangle(res2,(x,y),(x+w,y+h),(255,0,0),6)
            x1,y1 = ((x+(x+w))/2),((y+(y+h))/2)
            x1,y1 = int(x1),int(y1)
            if (y1<301):
                cnlist.append([x1,y1])
    print(cnlist)
    for i in cnlist:
        x1=i[0]
        y1=i[1]
        cv2.rectangle(img2,(x1-20,y1-20),(x1+20,y1+20),(255,0,0),6)
        plt.subplot(1,2,1)
        plt.imshow(img2)
        plt.show()
        print(x1,y1)
    return cnlist

def hbridge():
    GPIO.setmode (GPIO.BCM)
    GPIO.setwarnings (False)
    Ena, In1,In2=17,27,22
    GPIO.setup(Ena, GPIO.OUT)
    GPIO.setup(In1,GPIO.OUT)
    GPIO.setup(In2, GPIO.OUT)
    pwm = GPIO.PWM(Ena,100)
    pwm.start(0)
    while(True):
         GPIO.output(In1,GPIO.HIGH)
         GPIO.output(In2,GPIO.LOW)
         pwm.ChangeDutyCycle(25)
         time.sleep(3)
         GPIO.output(In1,GPIO.LOW)
         break
        
        
  
def xmotor(cnlist):
    GPIO_pinsy=(14,15,18)
    direction=20
    step = 21
    
    
    GPIO_pinsx=(13,19,26)
    direction_x=5
    step_x= 6
    mymotortestx = RpiMotorLib.A4988Nema(direction_x,step_x,GPIO_pinsx,"A4988")
    mymotortesty = RpiMotorLib.A4988Nema(direction,step,GPIO_pinsy,"A4988")
    cnlen=len(cnlist)
    pix=301
    while(cnlen>0):
        for i in cnlist:
            x1=i[0]
            y1=i[1]
            if(y1>301):
                continue
        #cv2.rectangle(img2,(x1-20,y1-20),(x1+20,y1+20),(255,0,0),6)
            print(x1,y1)
            prey=[301]
            ydp=prey[-1]-y1
            pix=pix-ydp
            prey.append(y1)
            '''if(y1<192):
                side=False            totaldist -= 500
                ydp=192-y1
            else:
                side=True
                ydp=y1-192'''
            slider=2
            xdist=int(((640-x1)/6.4)*50)
            ydist=int((ydp/6.4)*50)
            print(ydist)
            #totaldist=totaldist-500
            x = 0
            cnlen=cnlen-1
            while(x<2):
                if x==0:
                    print("Anti")
                    mymotortesty.motor_go(True, "Full",ydist,slider*.001, False, .05)
                    time.sleep(2)
                    mymotortestx.motor_go(True, "Full",xdist,slider*.001, False, .05)
                    time.sleep(2)
                    hbridge()
                    time.sleep(2)
                    #totaldist -= 500
        #print("Clock")
                    x=1
                elif x==1:
                    print("clock")
                    mymotortestx.motor_go(False,"Full", xdist, (slider)*.001, False, .05)
                    time.sleep(2)
                #mymotortesty.motor_go(not(side), "Full",ydist,slider*.001, False, .05)
                #time.sleep(2)
                    x=0
                    break
            print("----------------------------------")
    else:
        slider=2
        dist=int((pix/6.4)*50)
        mymotortesty.motor_go(True, "Full",dist,slider*.001, False, .05)
        time.sleep(2)
        pix=301
        #totaldist =totaldist- 500
        capture()
        cnlist=contour()
        xmotor(cnlist)
while(totaldist > 1):
    capture()
    cnlist=contour()
    xmotor(cnlist)
    break
    
