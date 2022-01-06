from djitellopy import tello
import KeyPressModule as kp
from time import sleep
import cv2
import time
import numpy as np
import math


rad2deg = 180/math.pi
deg2rad = math.pi/180

#########  PARAMETERS #########

fSpeed = 117/10 # Forward Speed in cm/s
aSpeed = 360/10 

dt = 0.25

dInterval = fSpeed*dt
aInterval = aSpeed*dt

###############################
x, y = 500, 500
a = 0
yaw = 0

trajectory = [(0,0)]

def getKeyboardInput(x, y, yaw, a):
    lr, fb, ud, yv = 0, 0, 0, 0

    rot_speed = 50
    trans_speed = 35
    d = 0

    if kp.getKey("a"):
        lr = -trans_speed
        d = dInterval
        a = -180
    elif kp.getKey("d"):
        lr = trans_speed
        d = -dInterval
        a = 180

    if kp.getKey("UP"):
        ud = trans_speed
    elif kp.getKey("DOWN"):
        ud = -trans_speed

    if kp.getKey("w"):
        fb = trans_speed
        d = dInterval
        a = 270
    elif kp.getKey("s"):
        fb = -trans_speed
        d = -dInterval
        a = -90

    if kp.getKey("LEFT"):
        yv = -rot_speed
        yaw -= aInterval
    elif kp.getKey("RIGHT"):
        yv = rot_speed
        yaw += aInterval

    if kp.getKey("e"):
        print("Taking off!")
        drone.takeoff()

    if kp.getKey("q"):
        print("Landing!")
        drone.land()

    if kp.getKey("z"):
        cv2.imwrite(f"Resources/Images/{time.time()}.jpg", img)
        sleep(0.3)
    
    sleep(dt)
    a += yaw
    x += int(d*math.cos(deg2rad*a))
    y += int(d*math.sin(deg2rad*a))
    return [lr, fb, ud, yv], x , y, yaw, a


def drawPoints(img, trajectory):
    for i in range(len(trajectory)):
        point = trajectory[i]
        cv2.circle(img, (point[0],point[1]),5,(0,0,255), cv2.FILLED)
    cv2.circle(img, (trajectory[-1][0], trajectory[-1][1]), 10, (0,255, 0), cv2.FILLED)
    cv2.putText(img, f"({(trajectory[-1][0]-500)/100}, {(trajectory[-1][1]-500)/100})m",(trajectory[-1][0]+10, trajectory[-1][1]+30), cv2.FONT_HERSHEY_PLAIN, 1, (255,100,125), 1)

kp.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())

drone.streamon()


sleep(5)

while True:
    vel_c, x, y, yaw, a = getKeyboardInput(x, y, yaw, a)
    drone.send_rc_control(vel_c[0], vel_c[1], vel_c[2], vel_c[3])

    if (x != trajectory[-1][0]) or (y != trajectory[-1][1]):
        trajectory.append([x, y])

    img = np.zeros((1000, 1000,3), np.uint8) # Create an array of values in 8 bit, that is ranging from 0 to 255 (an RGB grid)
    drawPoints(img, trajectory)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
    