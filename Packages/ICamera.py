class InterfaceCamera:
    from picamera import PiCamera
    import numpy as np

    def __init__(self, captureResolution = (1944,1944), outputResolution = (640,640)): 
        self.captureResolution = captureResolution
        # Rounds ouptut resolution to nearest 16
        self.outputResolution = (self.myround(outputResolution[0],16), self.myround(outputResolution[0],16))
        
        # Initialise camera
        self.camera = self.PiCamera()
        self.camera.resolution = self.captureResolution

    def myround(self, x, base=16):
        return base * round(x/base)

    


    # Takes a photo using picamera and returns the numpy array representing the image
    def getCapture(self):
        capture = self.np.empty((self.outputResolution[0], self.outputResolution[1], 3), dtype=self.np.uint8) # Resized resolution should be multiple of 16
        self.camera.capture(capture,'bgr', resize=(self.outputResolution[0], self.outputResolution[1]))
        return capture