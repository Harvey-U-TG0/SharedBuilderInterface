import picamera
import time

with picamera.PiCamera() as camera:
    camera.resolution = (2592, 1944)
    camera.rotation = 0
    camera.vflip = False
    camera.hflip = False
    time.sleep(1) # Camera warm-up time

    for i, filename in enumerate(camera.capture_continuous('images/image{counter:02d}.jpg')):
        print('Captured % filename')
        # Capture one image a minute
        time.sleep(5)
        if i==1000:
            break
