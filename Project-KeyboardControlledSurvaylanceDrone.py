from djitellopy import tello
import KeyPressModule as kp
from time import sleep
import cv2
import time

global img

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0

    rot_speed = 75
    trans_speed = 50

    if kp.getKey("a"):
        lr = -trans_speed
    elif kp.getKey("d"):
        lr = trans_speed

    if kp.getKey("UP"):
        ud = trans_speed
    elif kp.getKey("DOWN"):
        ud = -trans_speed

    if kp.getKey("w"):
        fb = trans_speed
    elif kp.getKey("s"):
        fb = -trans_speed

    if kp.getKey("LEFT"):
        yv = -rot_speed
    elif kp.getKey("RIGHT"):
        yv = rot_speed

    if kp.getKey("e"):
        print("Taking off!")
        drone.takeoff()

    if kp.getKey("q"):
        print("Landing!")
        drone.land()

    if kp.getKey("z"):
        cv2.imwrite(f"Resources/Images/{time.time()}.jpg", img)
        sleep(0.3)


    return [lr, fb, ud, yv]


kp.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())

drone.streamon()


sleep(5)

while True:
    vel_c = getKeyboardInput()
    drone.send_rc_control(vel_c[0], vel_c[1], vel_c[2], vel_c[3])

    img = drone.get_frame_read().frame
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (360, 240))

    cv2.imshow("Image", img)
    cv2.waitKey(1)

