import cv2
from djitellopy import tello
import KeyPressModule as kp
from time import sleep

### Basic Scheme for Controlling the Drone ###

# Takes inputs from keyboard and sends them as commands in the drones 4DOF: xyz and yaw
# x +- = ws   # y +- = da   # z +- = up/down-arrow   # yaw +- = right/left-arrow
# e = takeoff        # q = land

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
    
    return [lr, fb, ud, yv]


kp.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())

sleep(5)

while True:
    vel_c = getKeyboardInput()
    #print(vel_c)
    drone.send_rc_control(vel_c[0], vel_c[1], vel_c[2], vel_c[3])
    sleep(0.05)

