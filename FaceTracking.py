import cv2
import numpy as np
from djitellopy import tello
from time import sleep

w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0

def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListC = []
    myFaceListArea = []

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)

        cx = x + w // 2
        cy = y + h // 2

        area = w*h

        cv2.circle(img, (cx,cy), 5, (0,255,0),cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)
    
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0,0], 0]

def trackFace(drone, info, w, pid, pError):
    area = info[1]
    c = info[0]
    x , y = c[0], c[1]

    fb = 0
    error = x - w // 2
    speed = int(pid[0]*error + pid[1]*(error - pError))

    if abs(speed) > 100:
        speed = int(np.sign(speed)*100) # saturation on yaw speed

    if area > fbRange[0] and fbRange[1] < 6800:
        fb = 0 
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0

    #print(speed, fb)
    drone.send_rc_control(0,fb,0,speed)

    return error

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

#sleep(2)

drone.streamon()
drone.takeoff()

drone.send_rc_control(0, 0, 35, 0)
sleep(3)
drone.send_rc_control(0,0,0,0)



while True:
    img = drone.get_frame_read().frame
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (360, 240))

    img, info = findFace(img)

    pError = trackFace(drone, info, w, pid, pError)

    #print(f"Area: {info[1]}")
    #print(f"Center: {info[0]}")

    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        drone.land
        break