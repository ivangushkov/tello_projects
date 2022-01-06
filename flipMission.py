from djitellopy import tello
from time import sleep
import KeyPressModule as kp


drone = tello.Tello()

drone.connect()
print(drone.get_battery())

kp.init()



def mission():
    drone.takeoff()
    drone.flip_right()
    drone.send_rc_control(0,0,0,50)
    sleep(2)
    drone.send_rc_control(0,0,0,0)
    drone.land()

while True:
    if kp.getKey("e"):
        break

mission()

while True:
    if kp.getKey("q"):
        drone.land()

