# By Darshan
# 21/2/2018
# Purpose : To capture and store image with timer

from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import time
import cv2
import sys

#Text Properties
font = cv2.FONT_HERSHEY_SIMPLEX
textPosition= (180,240) #center
fontScale = 3
fontColor = (255,0,255)
lineType = 2

#Timer Properties
startCounter =  False
endCounter = False
incrementor = 0
total_Sec = 5


texxt = ['  3' ,'  2', '  1', 'Ready', 'Smile']

frame_incrementor = 0
determiner = 0

camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(2)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True ):
    image = frame.array

    frame_incrementor += 1

    determiner= frame_incrementor / 10

    if (int(determiner) == 1):
        incrementor +=1
        frame_incrementor=0

    if incrementor < total_Sec:
        cv2.putText(image,texxt[incrementor],textPosition,font,fontScale,fontColor,lineType)

    else:
        camera.capture('/home/pi/Desktop/Expression/Mouth_Data/bigopen.jpg')
        time.sleep(3)
        break


    cv2.imshow("FRAME", image)
    rawCapture.truncate(0)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break


camera.close()
cv2.destroyAllWindows()

