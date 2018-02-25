#   CREATED BY DARSHAN
#   PURPOSE : TO DETECT EXPRESSION IN REAL-TIME WEBCAM
#   DATE : FEB 22 ,3.34AM (START TIME)

from picamera.array import PiRGBArray
from picamera import PiCamera


from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import time
import imutils
import dlib
import cv2

def mouth_aspect_ratio(mouth):
    A=dist.euclidean(mouth[13], mouth[19])
    B=dist.euclidean(mouth[14], mouth[18])
    C=dist.euclidean(mouth[15], mouth[17])
    D=dist.euclidean(mouth[12], mouth[16])
    mar=(A+B+C)/(2.0 * D)
    return mar

MOUTH_STATE = [ 'OPEN' ,'NEUTRAL', 'CLOSED' ]
MOUTH_AR_THRESH_CLOSED = 0.10
MOUTH_AR_THRESH_OPENED = 0.20
MOUTH_AR_CONSEC_FRAME = 4

closed_Counter = 0
open_Counter = 0
#CLOSED = False
#OPENED = False
EXPRESSION_STATE = 'Neutral'

print("[INFO] : Loading Predictor...")
detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(mStart,mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

print("[INFO] : Warming camera...")


camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))


#vs=VideoStream(usePiCamera=1).start()
#fileStream=False
time.sleep(4)

print("[INFO] : Camera ready...?")
print("[INFO] : Rolliingggggg sirrr")


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True ):
    image = frame.array

    #image=imutils.resize(image,width=450)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects=detector(gray, 0)

    for rect in rects:
        shape=predictor(gray, rect)
        shape=face_utils.shape_to_np(shape)

        mouthPoint = shape[mStart:mEnd]
        mouthMAR = mouth_aspect_ratio(mouthPoint)

        for (x,y) in shape:
            cv2.circle(image, (x,y), 1,(0, 0, 255), -1)

        cv2.putText(image, "EAR: {:.2F}".format(mouthMAR), (300,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)

        if mouthMAR < MOUTH_AR_THRESH_CLOSED :
            #closed_Counter+=1
            EXPRESSION_STATE = 'CLOSED'

        elif mouthMAR > MOUTH_AR_THRESH_OPENED :
            #open_Counter += 1
            EXPRESSION_STATE = 'SMILE'

        '''else:
            if closed_Counter > MOUTH_AR_CONSEC_FRAME :
                EXPRESSION_STATE = 'CLOSED'
                closed_Counter = 0 
            elif open_Counter > MOUTH_AR_CONSEC_FRAME :
                EXPRESSION_STATE = 'OPENED'
                open_Counter = 0'''

        cv2.putText(image, "MOUTH STATE: {}".format(EXPRESSION_STATE), (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

    cv2.imshow("LIVE CAMERA",image)
    rawCapture.truncate(0)
    key=cv2.waitKey(1)&0xFF
    if key == ord("q"):
        break
        

camera.close()
cv2.destroyAllWindows()

'''
while True:
    frame=vs.read()
    frame=imutils.resize(frame,width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects=detector(gray, 0)

    for rect in rects:
        shape=predictor(gray, rect)
        shape=face_utils.shape_to_np(shape)

        mouthPoint = shape[mStart:mEnd]
        mouthMAR = mouth_aspect_ratio(mouthPoint)

        for (x,y) in shape:
            cv2.circle(frame, (x,y), 1,(0, 0, 255), -1)

        cv2.putText(frame, "EAR: {:.2F}".format(mouthMAR), (300,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)

        if mouthMAR < MOUTH_AR_THRESH_CLOSED :
            closed_Counter+=1

        elif mouthMAR > MOUTH_AR_THRESH_OPENED :
            open_Counter += 1

        else:
            if closed_Counter > MOUTH_AR_CONSEC_FRAME :
                EXPRESSION_STATE = 'CLOSED'
                closed_Counter = 0 
            elif open_Counter > MOUTH_AR_CONSEC_FRAME :
                EXPRESSION_STATE = 'OPENED'
                open_Counter = 0

        cv2.putText(frame, "MOUTH STATE: {}".format(EXPRESSION_STATE), (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

        cv2.imshow("Frame",frame)
        key=cv2.waitKey(1)&0xFF

        if key == ord("q"):
            break   
    

cv2.destroyAllWindows()
vs.stop()'''
    
