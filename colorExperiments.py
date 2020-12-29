from time import sleep
import numpy as np
from picamera import PiCamera
import cv2
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image

# Take photo


#with PiCamera() as camera:
#    camera.resolution = (2592, 1944)
#    camera.rotation = 0
#    camera.vflip = False
#    camera.hflip = False
#    sleep(2) # Camera warm-up time
#    camera.capture('images/image1.jpg')

studCount = 24

# Load image into CV
originalImg = cv2.imread('images/image1.jpg',1)

#Corner Coordinates
topLeft = np.array([922,711])
topRight = ([1700,695])
bottomLeft =([931,1497])
bottomRight =([1724,1484])
pt1 = np.float32([topLeft,topRight,bottomLeft,bottomRight])

# Set height and width of final image
height, width = 480, 480
pt2 = np.float32([[0,0],[width,0],[0,height],[width, height]])

# Warp the image
matrix = cv2.getPerspectiveTransform(pt1, pt2)
warpedImg = cv2.warpPerspective(originalImg, matrix, (width, height))
cv2.imwrite('images/warpedImg.png', warpedImg)

# Resize Image
resizedImg = cv2.resize(warpedImg, (studCount,studCount), interpolation=cv2.INTER_AREA)
cv2.imwrite('images/resizedImg.png', resizedImg)

# Convert to HSV
hsvImg = cv2.cvtColor(resizedImg,cv2.COLOR_BGR2HSV)

#returns a 1d array containing the average hsv values for  given 3d array
def averageHSV(array):
    hueTot = 0
    satTot = 0
    valTot = 0

    for rowIndex in range(array.shape[0]):
        for colIndex in range(array.shape [1]):

            hueTot += array[rowIndex,colIndex,0]
            satTot += array[rowIndex,colIndex,1]
            valTot += array[rowIndex,colIndex,2]

    hueAvg = hueTot/(array.shape[0]*array.shape[1])
    satAvg = satTot/(array.shape[0]*array.shape[1])
    valAvg = valTot/(array.shape[0]*array.shape[1])

    return(np.array([hueAvg,satAvg,valAvg]))


# Getting the HSV values of the calibration bricks
greenCalib = averageHSV(hsvImg[1:3,1:3])
blueCalib = averageHSV(hsvImg[1:3,3:5])
yellowCalib = averageHSV(hsvImg[1:3,5:7])
redCalib = averageHSV(hsvImg[1:3,7:9])

print("Green calibration is {}".format(greenCalib))
print("Blue calibration is {}".format(blueCalib))
print("Yellow calibration is {}".format(yellowCalib))
print("Red calibration is {}".format(redCalib))

# Setting ranges
greenHueRange = 15
greenSatRange = 60

greenHueMin = greenCalib[0]-greenHueRange
greenHueMax = greenCalib[0]+greenHueRange
greenHueMask = cv2.inRange(hsvImg, np.array([greenHueMin,0,0]), np.array([greenHueMax,255,255]))
cv2.imwrite('GreenMasks/greenHueMask.png', greenHueMask)

greenSatMin = greenCalib[1]-greenSatRange
greenSatMax = greenCalib[1]+greenSatRange
greenSatMask = cv2.inRange(hsvImg, np.array([0,greenSatMin,0]), np.array([180,greenSatMax,255]))
cv2.imwrite('GreenMasks/greenSatMask.png', greenSatMask)

greenBricks = np.zeros([studCount,studCount])
print (greenBricks)


#Add nested loops to Bitmask Add two requirements


# Visulisation
upscaledResizedImg = cv2.resize(resizedImg, (960,960), interpolation=cv2.INTER_AREA)
cv2.imwrite('images/upscaledResizedImg.png', upscaledResizedImg)

visImg = Image.open('images/upscaledResizedImg.png')

print ()
my_dpi=100

# Hue Figure
hueFig=plt.figure(figsize=(float(visImg.size[0])/my_dpi,float(visImg.size[1])/my_dpi),dpi=my_dpi)
ax=hueFig.add_subplot(111)

# Set the gridding interval: here we use the major tick interval
myInterval=40.
loc = plticker.MultipleLocator(base=myInterval)
ax.xaxis.set_major_locator(loc)
ax.yaxis.set_major_locator(loc)

# Add the grid
ax.grid(which='major', axis='both', linestyle='-', color='g')

# Add the image
ax.imshow(visImg)

# Add hue text for each grid
for rowIndex in range (hsvImg.shape[0]):
    for colIndex in range (hsvImg.shape [1]):
        ax.text(40*colIndex+5, 40*rowIndex+30, hsvImg[rowIndex,colIndex,0])

# Save the figure
hueFig.suptitle('Hue Values', fontsize=16)
hueFig.savefig('graphs/Hue figure.png')



# Saturation Figure
satFig=plt.figure(figsize=(float(visImg.size[0])/my_dpi,float(visImg.size[1])/my_dpi),dpi=my_dpi)
ax=satFig.add_subplot(111)

# Set the gridding interval: here we use the major tick interval
myInterval=40.
loc = plticker.MultipleLocator(base=myInterval)
ax.xaxis.set_major_locator(loc)
ax.yaxis.set_major_locator(loc)

# Add the grid
ax.grid(which='major', axis='both', linestyle='-', color='g')

# Add the image
ax.imshow(visImg)

# Add hue text for each grid
for rowIndex in range (hsvImg.shape[0]):
    for colIndex in range (hsvImg.shape [1]):
        ax.text(40*colIndex+5, 40*rowIndex+30, hsvImg[rowIndex,colIndex,1])

# Save the figure
satFig.suptitle('Saturuation Values', fontsize=16)
satFig.savefig('graphs/Satruation figure.png')



# Brightness Figure
briFig=plt.figure(figsize=(float(visImg.size[0])/my_dpi,float(visImg.size[1])/my_dpi),dpi=my_dpi)
ax=briFig.add_subplot(111)

# Set the gridding interval: here we use the major tick interval
myInterval=40.
loc = plticker.MultipleLocator(base=myInterval)
ax.xaxis.set_major_locator(loc)
ax.yaxis.set_major_locator(loc)

# Add the grid
ax.grid(which='major', axis='both', linestyle='-', color='g')

# Add the image
ax.imshow(visImg)

# Add hue text for each grid
for rowIndex in range (hsvImg.shape[0]):
    for colIndex in range (hsvImg.shape [1]):
        ax.text(40*colIndex+5, 40*rowIndex+30, hsvImg[rowIndex,colIndex,2])

# Save the figure
briFig.suptitle('Brightness Values', fontsize=16)
briFig.savefig('graphs/Brightness figure.png')