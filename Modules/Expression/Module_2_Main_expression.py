#   CREATED BY DARSHAN
#   PURPOSE : MAIN PROGRAM TO DETECT EXPRESSION PATTERN
#   DATE : FEB 26

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

#==============================================================================
#MODULES

#MODULE 1 : DISPLAY IMAGE

def module_1():
    img = cv2.imread("/home/pi/Pictures/Prototype1.jpg")
    cv2.imshow("cropped", img)
    cv2.waitKey(10)

#==============================================================================
#ALGORITHM SECTION

#EYE CONFIGURATION

def eye_aspect_ratio(eye):
    A=dist.euclidean(eye[1], eye[5])
    B=dist.euclidean(eye[2], eye[4])
    C=dist.euclidean(eye[0], eye[3])
    ear=(A+B)/(2.0 * C)
    return ear


#MOUTH CONFIGURATION

def mouth_aspect_ratio(mouth):
    A=dist.euclidean(mouth[13], mouth[19])
    B=dist.euclidean(mouth[14], mouth[18])
    C=dist.euclidean(mouth[15], mouth[17])
    D=dist.euclidean(mouth[12], mouth[16])
    mar=(A+B+C)/(2.0 * D)
    return mar

#-----------------------------------------------------------------------------

EYE_AR_THRESH=0.3
EYE_AR_CONSEC_FRAMES = 48 # DEYYYYY CHANGE THIS TO 48 LATER !!!!!
COUNTER=0
TOTAL=0

MOUTH_STATE = [ 'OPEN' ,'NEUTRAL', 'CLOSED' ]
MOUTH_AR_THRESH_CLOSED = 0.10
MOUTH_AR_THRESH_OPENED = 0.20
MOUTH_AR_CONSEC_FRAME = 10
MOUTH_OPEN = False
MOUTH_CLOSED = False

MOUTH_OPEN_TOTAL = 0 #TO KEEP TRACK ON NUMBER OF MOUTH CLOSED
activate_Module_1 = False
#-----------------------------------------------------------------------------


RIGHT_COUNTER= 0    # TO KEEP TRACK ON NUMBER OF CLOSED RIGHT EYES
RIGHT_TOTAL= 0      # TO COUNT THE NUMBER OF RIGHT EYE BLINK OVER CERTAIN FRAME
RIGHT_CLOSE=False   # THE STATE OF RIGHT EYE , TRUE MEANS CLOSE , FALSE MEANS OPEN


LEFT_COUNTER = 0    # TO KEEP TRACK ON NUMBER OF CLOSED LEFT EYES
LEFT_TOTAL=0        # TO COUNT THE NUMBER OF LEFT EYE BLINK OVER CERTAIN FRAME
LEFT_CLOSE=False    # THE STATE OF LEFT EYE , TRUE MEANS CLOSE , FALSE MEANS OPEN


closed_Counter = 0
open_Counter = 0
#CLOSED = False
#OPENED = False
EXPRESSION_STATE = 'Neutral'

modules = ['MAIN MODULE','TIME MODULE','WEATHER MODUL','SCHEDULE MODULE','NEWS MODULE']




#==============================================================================

#PROGRAM START

print("[INFO] : Loading Predictor...")
detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(lStart,lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart,rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart,mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

print("[INFO] : Warming camera...")


camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
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

        leftEye=shape[lStart:lEnd]
        rightEye=shape[rStart:rEnd]
        mouthPoint = shape[mStart:mEnd]

        leftEAR=eye_aspect_ratio(leftEye)
        rightEAR=eye_aspect_ratio(rightEye)        
        mouthMAR = mouth_aspect_ratio(mouthPoint)

        for (x,y) in shape:
            cv2.circle(image, (x,y), 1,(0, 0, 255), -1)

        leftEyeHull=cv2.convexHull(leftEye)
        rightEyeHull=cv2.convexHull(rightEye)
        mouthEyeHull=cv2.convexHull(mouthPoint)
        cv2.drawContours(image,[leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(image,[rightEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(image,[mouthEyeHull], -1, (0, 255, 0), 1)

        cv2.putText(image, "EAR: {:.2F}".format(mouthMAR), (300,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)
        
        if mouthMAR < MOUTH_AR_THRESH_CLOSED :
            closed_Counter+=1
            EXPRESSION_STATE = 'CLOSED'
            activate_Module = "same"

        elif mouthMAR > MOUTH_AR_THRESH_OPENED :
            open_Counter += 1
            EXPRESSION_STATE = 'SMILE'
            if open_Counter >= MOUTH_AR_CONSEC_FRAME :     # IF MOUTH-OPEN FRAME EXCEEDED 2 SEC
                activate_Module_1 = True
                break
                #MOUTH_OPEN = True                           # SET MOUTH IS OPEN
                activate_Module = "activate win1"                # ACTIVATE WEATHER MODULE
                #open_Counter = 0                            # RESET COUNTER
                #MOUTH_OPEN_TOTAL += 1                       # KEEP TRACK ON NUMBER OF TIMES MOUTH IS VERIFIED OPEN
            else:
                activate_Module = "same"               # MAINTAIN THIS MAIN PROGRAM

        
        
        cv2.putText(image, "open_Counter: {}".format(open_Counter), (200,100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        cv2.putText(image, "MOUTH STATE: {}".format(EXPRESSION_STATE), (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        cv2.putText(image, "ACTIVATE MODULE: {}".format(activate_Module), (10,100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
    
    cv2.imshow("LIVE CAMERA",image)
    rawCapture.truncate(0)
    if activate_Module_1 == True:
        break
    key=cv2.waitKey(1)&0xFF
    if key == ord("q"):
        break

camera.close()
cv2.destroyAllWindows()
        
if activate_Module_1 == True:
    img = cv2.imread("/home/pi/Pictures/Prototype1.jpg")
    cv2.imshow("cropped", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



'''
if closed_Counter >= MOUTH_AR_CONSEC_FRAME :
            MOUTH_CLOSED = True
            closed_Counter = 0

        if open_Counter > MOUTH_AR_CONSEC_FRAME :
            MOUTH_OPEN = True
            open_Counter = 0


        if MOUTH_CLOSED == True:
            activate_Module = modules[1]
            MOUTH_OPEN =False
        else:
            if MOUTH_OPEN == True:
                activate_Module = modules[2]
                MOUTH_CLOSED = False
            else:
                activate_Module = modules[0]
                MOUTH_CLOSED = False
                MOUTH_OPEN = False 




        else:
            EXPRESSION_STATE = "NEUTRAL"
            closed_Counter = 0
            open_Counter = 0
            activate_Module = "same"'''


'''     if leftEAR<EYE_AR_THRESH:   #IF EYE CLOSED , INCREASE AN INCREMENT
            LEFT_COUNTER+=1

        else:   #WHEN EYE IN OPEN STATE, COUNT THE INCREMENT AND COMPARE WITH NUMBER OF FRAME
        
            if LEFT_COUNTER >=EYE_AR_CONSEC_FRAMES: #IF EYE IN CLOSED STATE FOR CERTAIN FRAME
                LEFT_TOTAL+=1                       # IT CONSIDERED AS LEFT BLINK 
                LEFT_CLOSE = True
                LEFT_COUNTER=0  # RESET INCREMENT FOR LEFT EYE


        if rightEAR<EYE_AR_THRESH:
            RIGHT_COUNTER+=1
            
        else:
            if RIGHT_COUNTER >=EYE_AR_CONSEC_FRAMES:
                RIGHT_TOTAL+=1
                RIGHT_COUNTER=0
                RIGHT_CLOSE = True
'''

    
