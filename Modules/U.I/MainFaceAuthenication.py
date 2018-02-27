from face_recognition import FACE_RECOGNITION
from u1_face_recognition import UI_MAIN_1
from u1_face_recognition import UI_MAIN_2

UI_MAIN_1()

permission = FACE_RECOGNITION()

if permission == True:
    UI_MAIN_2()
else:
    print("FAILED")
