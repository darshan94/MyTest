import cv2

def UI_MAIN_1():
    img = cv2.imread("/home/pi/Pictures/u1.png")
    cv2.namedWindow("Face_Recognition",cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Face_Recognition",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Face_Recognition", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def UI_MAIN_2():
    img = cv2.imread("/home/pi/Pictures/u2.png")
    cv2.namedWindow("Face_Recognition",cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Face_Recognition",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Face_Recognition", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def UI_MAIN_3():
    img = cv2.imread("/home/pi/Pictures/u3.png")
    cv2.namedWindow("WEATHER",cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("WEATHER",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("WEATHER", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def UI_MAIN_4():
    img = cv2.imread("/home/pi/Pictures/u4.png")
    cv2.namedWindow("CALENDAR",cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("CALENDAR",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("CALENDAR", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def UI_MAIN_5():
    mg = cv2.imread("/home/pi/Pictures/u4.png")
    cv2.namedWindow("CALENDAR",cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("CALENDAR",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("CALENDAR", mg)
    img = cv2.imread("/home/pi/Pictures/Prototype1.jpg")
    cv2.namedWindow("SELFIE")
    #cv2.setWindowProperty("SELFIE",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("SELFIE", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    

UI_MAIN_5()
