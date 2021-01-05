from time import sleep
from picamera import PiCamera
import signal
import numpy as np
import cv2


takePhotos = True

def InteruptHandler(signal, frame):
    global takePhotos 
    takePhotos = False



camera = PiCamera()
camera.resolution = (1944, 1944)
sleep(2)


# Register signal handler
signal.signal(signal.SIGINT, InteruptHandler)

while(True):
    if (takePhotos == False):
        break
    image = np.empty((640, 640, 3), dtype=np.uint8)
    camera.capture(image,'bgr', resize=(640, 640))
    cv2.imwrite('TestImages/piCapture.png', image)








#with PiCamera() as camera:
#    camera.resolution = (2592, 1944)
#    camera.rotation = 0
#    camera.vflip = False
#    camera.hflip = False
#    sleep(2) # Camera warm-up time
#    camera.capture('images/image1.jpg')


