from time import sleep
import numpy as np
from picamera import PiCamera
import cv2
import sys
sys.path.append('/home/pi/Git/SharedBuilderInterface/Packages')
sys.path.append('/home/pi/Git/SharedBuilderInterface/TestData')
sys.path.append('/home/pi/Git/SharedBuilderInterface/Data')

from API import InterfaceAPI
from testData import ITestData
from ICamera import InterfaceCamera
from InterfaceCV import BuildPlateComprehension
from Data import appData
from BrickProcessing import BrickComprehension

# Save debug images, slows down program significantly
debug = False
imageDataFilePath = 'ImageData/UpdateSteps/'

# Server Communications
serverAddress = 'http://192.168.1.73:5000/'
deviceUsername = 'Emily'

# Create an InterfaceAPI object that will be used for server communications
interface = InterfaceAPI(serverAddress,deviceUsername)


# Create an instance of the camera object
camera = InterfaceCamera(300)

# Create build plate comprehension object
cVObject = BuildPlateComprehension()

# Create brick processor object
brickProcessor = BrickComprehension()

# Take a photo

# Run image comprehension to return an array of stud types (input: raw image)

# Output brick configuration (input: comprehended image + current brick configuration)


# Hardwear settings
# topLeft, topRight, bottom left, bottom right
photoCornerCords = np.array([[125,156],[499,161],[122,533],[496,533]])
buildPlateDimensions = (12,12) # Should always be stored as a tuple
idCalibrationMap=np.array([[9,9,6,6,5,5,5,5,9,9,6,6],
                           [9,9,6,6,5,5,5,5,9,9,6,6],
                           [8,8,7,7,5,5,5,5,8,8,7,7],
                           [8,8,7,7,5,5,5,5,8,8,7,7],
                           [5,5,5,5,5,5,5,5,5,5,5,5],
                           [5,5,5,5,5,5,5,5,5,5,5,5],
                           [5,5,5,5,5,5,5,5,5,5,5,5],
                           [5,5,5,5,5,5,5,5,5,5,5,5],
                           [9,9,6,6,5,5,5,5,9,9,6,6],
                           [9,9,6,6,5,5,5,5,9,9,6,6],
                           [8,8,7,7,5,5,5,5,8,8,7,7],
                           [8,8,7,7,5,5,5,5,8,8,7,7],
                            ])


# CV parameters
hSVRegionAcceptence = (20,20,20)

colourCalibRef=[
        {
            'colourID': 6, # ID number for colour
            'hsv': (179,185,150), # HSV of colour in photos
            'hsvRange':(20,20,20), # HSV ranges for acceptance
        }
        ]



#   Get a new photo
capture = camera.getCapture()
if (debug): cv2.imwrite(imageDataFilePath + 'capture.png', capture)

# Warp Image
warpedImg= cVObject.warpToBuildPlateFromCords(capture,photoCornerCords)
if (debug): cv2.imwrite(imageDataFilePath + 'warpedImg.png', warpedImg)

# Resize Image
resizedImg = cv2.resize(warpedImg, buildPlateDimensions, interpolation=cv2.INTER_AREA)
if (debug): cv2.imwrite(imageDataFilePath + 'resisedImg.png', resizedImg)

# Convert to HSV
hsvImg = cv2.cvtColor(resizedImg,cv2.COLOR_BGR2HSV)
if (debug): cv2.imwrite(imageDataFilePath + 'hsvImg.png', hsvImg)


# calibrate colour references
colourCalibRef = cVObject.getCalibration(hsvImg, idCalibrationMap)
print (colourCalibRef)





# Get brick references and add outlines
bricksRef = brickProcessor.generateBrickOutlines(appData.bricksRef)

brickConfig = []






# Update 
def update():
    #   Get a new photo
    capture = camera.getCapture()
    if (debug): cv2.imwrite(imageDataFilePath + 'capture.png', capture)

    # Warp Image
    warpedImg= cVObject.warpToBuildPlateFromCords(capture,photoCornerCords)
    if (debug): cv2.imwrite(imageDataFilePath + 'warpedImg.png', warpedImg)

    # Resize Image
    resizedImg = cv2.resize(warpedImg, buildPlateDimensions, interpolation=cv2.INTER_AREA)
    if (debug): cv2.imwrite(imageDataFilePath + 'resisedImg.png', resizedImg)

    # Convert to HSV
    hsvImg = cv2.cvtColor(resizedImg,cv2.COLOR_BGR2HSV)
    if (debug): cv2.imwrite(imageDataFilePath + 'hsvImg.png', hsvImg)

    # Run image comprehension code
    studConfiguration = cVObject.getPlateConfig(hsvImg,resizedImg,buildPlateDimensions,hSVRegionAcceptence,colourCalibRef,appData.studColourIDMappings,appData.cIDtoBGR,imageDataFilePath,debug)

    #   Understand brick configuration
    
    # Generate usability map
    usabilityMap = brickProcessor.generateUsabilityMap(studConfiguration)

    # Remove unneded bricks
    brickConfigRemoved = brickProcessor.removeBricks(studConfiguration, usabilityMap, brickConfig)

    usedUpMap = brickProcessor.generateUsedUpMap(brickConfigRemoved,bricksRef,studConfiguration.shape)

    finalBrickConfig = brickProcessor.addBricks(studConfiguration,usabilityMap, brickConfigRemoved, bricksRef)
    
    #   Upload to server
    #interface.postData(ITestData.arrangementA)


# Call update loop once


for i in range(20):
    update()

for brick in brickConfig:
    print (brick)