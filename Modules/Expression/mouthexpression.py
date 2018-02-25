#BY DARSHAN
#AIM : TO EXTRACT DATA FOR MOUTH EXPRESSION ALGORITHM
#DATE : 22/2/2018

from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np
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

detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(mStart,mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

image = cv2.imread("/home/pi/Desktop/Expression/Mouth_Data/smile.jpg")
image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
rects = detector(gray, 1)

for rect in rects:
    shape=predictor(gray, rect)
    shape=face_utils.shape_to_np(shape)

    mouthPoint = shape[mStart:mEnd]
    mouthMAR = mouth_aspect_ratio(mouthPoint)

    for (x,y) in shape:
        cv2.circle(image, (x,y), 1,(0, 0, 255), -1)

    cv2.putText(image, "EAR: {:.2F}".format(mouthMAR), (300,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)

cv2.imshow("OUTPUT", image)
cv2.waitKey(0)

