from djitellopy import tello
import cv2
from time import sleep

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

sleep(1)
drone.streamon()

while True:
    img = drone.get_frame_read().frame
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (360, 240))

    cv2.imshow("Image", img)
    cv2.waitKey(1)