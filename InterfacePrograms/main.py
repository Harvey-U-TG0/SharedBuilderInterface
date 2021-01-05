from time import sleep
import numpy as np
from picamera import PiCamera
import cv2
import sys
sys.path.append('/home/pi/Git/SharedBuilderInterface/Packages')
sys.path.append('/home/pi/Git/SharedBuilderInterface/TestData')

from API import InterfaceAPI
from testData import ITestData
from ICamera import InterfaceCamera



# Server Communications
serverAddress = 'http://192.168.1.73:5000/'
deviceUsername = 'Emily'

# Create an InterfaceAPI object that will be used for server communications
interface = InterfaceAPI(serverAddress,deviceUsername)


# Create an instance of the camera object
camera = InterfaceCamera()

# Take a photo

# Run image comprehension to return an array of stud types (input: raw image)

# Output brick configuration (input: comprehended image + current brick configuration)




# Update 
#   Get a new photo
capture = camera.getCapture()

#   Run image comprehension code

#   Understand brick configuration

#   Upload to server
interface.postData(ITestData.arrangementA)


