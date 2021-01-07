from time import sleep

class InterfaceCamera:
    from picamera import PiCamera
    import numpy as np

    def __init__(self, isoValue=300, captureResolution = (1944,1944), outputResolution = (640,640)): 
        self.captureResolution = captureResolution
        # Rounds ouptut resolution to nearest 16
        self.outputResolution = (self.myround(outputResolution[0],16), self.myround(outputResolution[0],16))
        
        # Initialise camera
        self.camera = self.PiCamera()
        self.camera.resolution = self.captureResolution
        self.camera.framerate = 5
        self.camera.iso = isoValue
        # Wait for the automatic gain control to settle
        sleep(2)
        # Now fix the values
        self.camera.shutter_speed = self.camera.exposure_speed
        self.camera.exposure_mode = 'off'
        g = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = g


    def myround(self, x, base=16):
        return base * round(x/base)

    


    # Takes a photo using picamera and returns the numpy array representing the image
    def getCapture(self):
        capture = self.np.empty((self.outputResolution[0], self.outputResolution[1], 3), dtype=self.np.uint8) # Resized resolution should be multiple of 16
        self.camera.capture(capture,'bgr', resize=(self.outputResolution[0], self.outputResolution[1]))
        return capture