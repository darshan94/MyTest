from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import datetime
import time
import imutils
import dlib
import cv2





detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

'''def landmarker(frameImage):
    detections=detector(frameImage, 1)
    for k,d in enumerate(detections):
        shape=predictor(frameImage, d)
        xlist.append=[]
        ylist.append=[]
        for i in range(1,68):
            xlist.append(float(shape.part(i).x))
            ylist.append(float(shape.part(i).y))

            for x, y in zip(xlist,ylist):
                landmarks.append(x)
                landmarks.append(y)

        if len(detecti'''



print("[INFO] : Warming camera...")

vs=VideoStream(usePiCamera=1).start()
time.sleep(4)

print("[INFO] : Camera ready...")

while True:
    frame=vs.read()
    print("[INFO] : Camera took a frame...")
    frame=imutils.resize(frame,width=400)
    print("[INFO] : Warming camera...")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print("[INFO] : Detecting face in a frame...")
    rects=detector(gray, 0)

    for rect in rects:
        shape=predictor(gray, rect)
        shape=face_utils.shape_to_np(shape)

        
        for (x,y) in shape:
                cv2.circle(frame, (x,y), 1,(0, 0, 255), -1)
           
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
        
        
    

cv2.destroyAllWindows()
vs.stop()
        

    
    
