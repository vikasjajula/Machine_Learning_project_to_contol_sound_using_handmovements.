import cv2
import math
import numpy as np
import mediapipe as mp
from ctypes import cast,POINTER #used to control the audio volume
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities , IAudioEndpointVolume # used to provide interface for audio speaker arrangements

cap = cv2.VideoCapture(0) # to take input from the camera of the device
pTime =0
cTime =0
mpHands= mp.solutions.hands
mpDraws= mp.solutions.drawing_utils
hands=mpHands.Hands()
devices = AudioUtilities.GetSpeakers() # retrives the audio outputs in the system.
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None) # casts the interface to an pointer , which allows controlling the volume.
volume = cast(interface , POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol= volRange[0]
maxVol= volRange[2]
print(volRange)
print(minVol)
print(maxVol)
while True:
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # mediapipe requires only RGB image to process
    results= hands.process(imgRGB) # Detects the hand in the image and the landmarks using the hand traking model.
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmlist=[]
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                mpDraws.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            if lmlist:
                x1,y1= lmlist[4][1] , lmlist[4][2]
                x2,y2= lmlist[8][1] , lmlist[8][2]
                print(x1,y1)
                print(x2,y2)
                cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
                cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)

                cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
                #mid point of the line from thump tip to index fingure tip
                z1= (x1+x2)//2
                z2=(y1+y2)//2

                cv2.circle(img ,(z1,z2),15,(255,0,255),cv2.FILLED)
                length= math.hypot(x2-x1,y2-y1)

                if length < 50:
                    cv2.circle(img, (z1, z2), 15, (255, 0, 255), cv2.FILLED)
            vol= np.interp(length ,[50,300],[minVol,maxVol])
            volBar = np.interp(length , [50,300] , [400,150])
            volPer = np.interp(length,[50,300],[0,100])

            print(int(length),vol)
            volume.SetMasterVolumeLevel(vol,None)

            cv2.rectangle(img,(50,150),(85,400) , (0,255,0) ,3)
            cv2.rectangle(img,(50,int(volBar)),(85,400) ,(0,255,0),cv2.FILLED)
            cv2.putText(img , f'{int(volPer)}%',(40,450), cv2.FONT_HERSHEY_PLAIN,3,(0,255,255),3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)









