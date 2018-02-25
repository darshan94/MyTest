from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import time
import imutils
import dlib
import cv2

def eye_aspect_ratio(eye):
    A=dist.euclidean(eye[1], eye[5])
    B=dist.euclidean(eye[2], eye[4])
    C=dist.euclidean(eye[0], eye[3])
    ear=(A+B)/(2.0 * C)
    return ear


def prototype_exp(lefteye,righteye):
    if(lefteye==0,righteye==1):
        result="Exp 1"
    elif(letfeye==1,righteye==0):
        result="EXp 2"
    return result

EYE_AR_THRESH=0.3
EYE_AR_CONSEC_FRAMES = 3 # DEYYYYY CHANGE THIS TO 48 LATER !!!!!
COUNTER=0
TOTAL=0

RIGHT_COUNTER= 0    # TO KEEP TRACK ON NUMBER OF CLOSED RIGHT EYES
RIGHT_TOTAL= 0      # TO COUNT THE NUMBER OF RIGHT EYE BLINK OVER CERTAIN FRAME
RIGHT_CLOSE=False   # THE STATE OF RIGHT EYE , TRUE MEANS CLOSE , FALSE MEANS OPEN


LEFT_COUNTER = 0    # TO KEEP TRACK ON NUMBER OF CLOSED LEFT EYES
LEFT_TOTAL=0        # TO COUNT THE NUMBER OF LEFT EYE BLINK OVER CERTAIN FRAME
LEFT_CLOSE=False    # THE STATE OF LEFT EYE , TRUE MEANS CLOSE , FALSE MEANS OPEN





print("[INFO] : Loading Predictor...")
detector=dlib.get_frontal_face_detector() #to detect face
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") # to mark landpoint on face

(lStart,lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart,rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


print("[INFO] : Warming camera...")

vs=VideoStream(usePiCamera=1).start()
fileStream=False
time.sleep(4)

print("[INFO] : Camera ready...?")
print("[INFO] : Rolliingggggg sirrr")

while True:
    frame=vs.read()
    frame=imutils.resize(frame,width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects=detector(gray, 0)

    for rect in rects:
        shape=predictor(gray, rect)
        shape=face_utils.shape_to_np(shape)

        leftEye=shape[lStart:lEnd]
        rightEye=shape[rStart:rEnd]

        leftEAR=eye_aspect_ratio(leftEye)
        rightEAR=eye_aspect_ratio(rightEye)

        ear=(leftEAR+rightEAR)/2.0

        leftEyeHull=cv2.convexHull(leftEye)
        rightEyeHull=cv2.convexHull(rightEye)
        cv2.drawContours(frame,[leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame,[rightEyeHull], -1, (0, 255, 0), 1)

        if leftEAR<EYE_AR_THRESH:   #IF EYE CLOSED , INCREASE AN INCREMENT
            LEFT_COUNTER+=1

        else:   #WHEN EYE IN OPEN STATE, COUNT THE INCREMENT AND COMPARE WITH NUMBER OF FRAME
        
            if LEFT_COUNTER >=EYE_AR_CONSEC_FRAMES: #IF EYE IN CLOSED STATE FOR CERTAIN FRAME
                LEFT_TOTAL+=1                       # IT CONSIDERED AS LEFT BLINK 
                '''if not leftClose: 
                    leftClose=True'''
                LEFT_COUNTER=0  # RESET INCREMENT FOR LEFT EYE


        if rightEAR<EYE_AR_THRESH:
            RIGHT_COUNTER+=1
            
        else:
            if RIGHT_COUNTER >=EYE_AR_CONSEC_FRAMES:
                RIGHT_TOTAL+=1
                RIGHT_COUNTER=0
                
        #trigger = prototype_exp(lEye,rEye)
        cv2.putText(frame, "Blinks: {}".format(TOTAL), (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        cv2.putText(frame, "EAR: {:.2F}".format(ear), (300,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)
        cv2.putText(frame, "LEFT EAR: {:.2F}".format(leftEAR), (300,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)
        cv2.putText(frame, "RIGHT EAR: {:.2F}".format(rightEAR), (300,90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)
        cv2.putText(frame, "LeftEyeBlink: {}".format(LEFT_TOTAL), (10,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        cv2.putText(frame, "RightEyeBlink: {}".format(RIGHT_TOTAL), (10,90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

    cv2.imshow("Frame",frame)
    key=cv2.waitKey(1)&0xFF

    if key == ord("q"):
        break   
    

cv2.destroyAllWindows()
vs.stop()

