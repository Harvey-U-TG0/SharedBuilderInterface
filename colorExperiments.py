from time import sleep
import numpy as np
from picamera import PiCamera
import cv2
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image
from timeit import default_timer as timer



# ...




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
originalImg = cv2.imread('images/HandTestA.jpeg',1)

start = timer()

#Corner Coordinates
topLeft = np.array([343,230])
topRight = ([724,242])
bottomLeft =([324,616])
bottomRight =([719,631])
pt1 = np.float32([topLeft,topRight,bottomLeft,bottomRight])

# Set height and width of final image
height, width = 480, 480
pt2 = np.float32([[0,0],[width,0],[0,height],[width, height]])

# Warp the image
matrix = cv2.getPerspectiveTransform(pt1, pt2)
warpedImg = cv2.warpPerspective(originalImg, matrix, (width, height))
#cv2.imwrite('images/warpedImg.png', warpedImg)

# Resize Image
resizedImg = cv2.resize(warpedImg, (studCount,studCount), interpolation=cv2.INTER_AREA)
#cv2.imwrite('images/resizedImg.png', resizedImg)

# Convert to HSV
hsvImg = cv2.cvtColor(resizedImg,cv2.COLOR_BGR2HSV)

#returns a 1d array containing the average hsv values for  given 3d array
# Slice hue is used for red and will add on 180 to values below 90
def averageHSV(array,sliceHue = False):
    hueTot = 0
    satTot = 0
    valTot = 0

    for rowIndex in range(array.shape[0]):
        for colIndex in range(array.shape [1]):
            hueValue = array[rowIndex,colIndex,0]
            if (sliceHue) and (hueValue<90):
                hueValue += 180
                print(hueValue)

            hueTot += hueValue
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
redCalib = averageHSV(hsvImg[1:3,7:9],sliceHue = True) # Special red hue calculation due to centre at 180
blankCalib = averageHSV(hsvImg[1:3,10:12]) # The calibration value for tiles with no bricks on or shadow

print("Green calibration is {}".format(greenCalib))
print("Blue calibration is {}".format(blueCalib))
print("yellow calibration is {}".format(yellowCalib))
print("Red calibration is {}".format(redCalib))
print("Blank calibration is {}".format(blankCalib))

# Setting ranges, The + or - range from the detected mean from the calibration blocks
greenHueRange = 15
greenSatRange = 60
greenBriRange = 40

greenHueMin = greenCalib[0]-greenHueRange
greenHueMax = greenCalib[0]+greenHueRange
greenHueMask = cv2.inRange(hsvImg, np.array([greenHueMin,0,0]), np.array([greenHueMax,255,255]))
#cv2.imwrite('GreenMasks/greenHueMask.png', greenHueMask)

greenSatMin = greenCalib[1]-greenSatRange
greenSatMax = greenCalib[1]+greenSatRange
greenSatMask = cv2.inRange(hsvImg, np.array([0,greenSatMin,0]), np.array([180,greenSatMax,255]))
#cv2.imwrite('GreenMasks/greenSatMask.png', greenSatMask)

greenBriMin = greenCalib[2]-greenBriRange
greenBriMax = greenCalib[2]+greenBriRange
greenBriMask = cv2.inRange(hsvImg, np.array([0,0,greenBriMin]), np.array([180,255,greenBriMax]))
#cv2.imwrite('GreenMasks/greenBriMask.png', greenBriMask)

greenBricks = np.zeros([studCount,studCount])

#Add nested loops to Bitmask Add two requirements
for rowIndex in range(greenBricks.shape[0]):
    for colIndex in range(greenBricks.shape [1]):
        if (greenHueMask[rowIndex,colIndex] == 255) and (greenSatMask[rowIndex,colIndex] == 255) and (greenBriMask[rowIndex,colIndex] == 255):
            greenBricks[rowIndex,colIndex] = 1

#cv2.imwrite('GreenMasks/GreenBricks.png', greenBricks*255)


blueHueRange = 10
blueSatRange = 80
blueBriRange = 28

blueHueMin = blueCalib[0]-blueHueRange
blueHueMax = blueCalib[0]+blueHueRange
blueHueMask = cv2.inRange(hsvImg, np.array([blueHueMin,0,0]), np.array([blueHueMax,255,255]))
#cv2.imwrite('BlueMasks/blueHueMask.png', blueHueMask)

blueSatMin = blueCalib[1]-blueSatRange
blueSatMax = blueCalib[1]+blueSatRange
blueSatMask = cv2.inRange(hsvImg, np.array([0,blueSatMin,0]), np.array([180,blueSatMax,255]))
#cv2.imwrite('BlueMasks/blueSatMask.png', blueSatMask)

blueBriMin = blueCalib[2]-blueBriRange
blueBriMax = blueCalib[2]+blueBriRange
blueBriMask = cv2.inRange(hsvImg, np.array([0,0,blueBriMin]), np.array([180,255,blueBriMax]))
#cv2.imwrite('BlueMasks/blueBriMask.png', blueBriMask)

blueBricks = np.zeros([studCount,studCount])

#Add nested loops to Bitmask Add two requirements
for rowIndex in range(blueBricks.shape[0]):
    for colIndex in range(blueBricks.shape [1]):
        if (blueHueMask[rowIndex,colIndex] == 255) and (blueSatMask[rowIndex,colIndex] == 255) and (blueBriMask[rowIndex,colIndex] == 255):
            blueBricks[rowIndex,colIndex] = 1

#cv2.imwrite('BlueMasks/blueBricks.png', blueBricks*255)


yellowHueRange = 3
yellowSatRange = 115
yellowBriRange = 38

yellowHueMin = yellowCalib[0]-yellowHueRange
yellowHueMax = yellowCalib[0]+yellowHueRange
yellowHueMask = cv2.inRange(hsvImg, np.array([yellowHueMin,0,0]), np.array([yellowHueMax,255,255]))
#cv2.imwrite('YellowMasks/yellowHueMask.png', yellowHueMask)

yellowSatMin = yellowCalib[1]-yellowSatRange
yellowSatMax = yellowCalib[1]+yellowSatRange
yellowSatMask = cv2.inRange(hsvImg, np.array([0,yellowSatMin,0]), np.array([180,yellowSatMax,255]))
#cv2.imwrite('YellowMasks/yellowSatMask.png', yellowSatMask)

yellowBriMin = yellowCalib[2]-yellowBriRange
yellowBriMax = yellowCalib[2]+yellowBriRange
yellowBriMask = cv2.inRange(hsvImg, np.array([0,0,yellowBriMin]), np.array([180,255,yellowBriMax]))
#cv2.imwrite('YellowMasks/yellowBriMask.png', yellowBriMask)

yellowBricks = np.zeros([studCount,studCount])

#Add nested loops to Bitmask Add two requirements
for rowIndex in range(yellowBricks.shape[0]):
    for colIndex in range(yellowBricks.shape [1]):
        if (yellowHueMask[rowIndex,colIndex] == 255) and (yellowSatMask[rowIndex,colIndex] == 255) and (yellowBriMask[rowIndex,colIndex] == 255):
            yellowBricks[rowIndex,colIndex] = 1

#cv2.imwrite('YellowMasks/yellowBricks.png', yellowBricks*255)


redHueRange = 5
redSatRange = 36
redBriRange = 55

redHueMin = redCalib[0]-redHueRange
redHueMax = redCalib[0]+redHueRange

# Special accounting for red due to looping at 180
if (redHueMax >180) and (redHueMin<180):

    redHueMaskMin = cv2.inRange(hsvImg, np.array([redHueMin,0,0],dtype='uint8'), np.array([180,255,255],dtype='uint8'))
    redHueMaskMax = cv2.inRange(hsvImg, np.array([0,0,0],dtype='uint8'), np.array([redHueMax-180,255,255],dtype='uint8'))
    redHueMask = redHueMaskMin+redHueMaskMax

#cv2.imwrite('RedMasks/redHueMask.png', redHueMask)

redSatMin = redCalib[1]-redSatRange
redSatMax = redCalib[1]+redSatRange
redSatMask = cv2.inRange(hsvImg, np.array([0,redSatMin,0]), np.array([180,redSatMax,255]))
#cv2.imwrite('RedMasks/redSatMask.png', redSatMask)

redBriMin = redCalib[2]-redBriRange
redBriMax = redCalib[2]+redBriRange
redBriMask = cv2.inRange(hsvImg, np.array([0,0,redBriMin]), np.array([180,255,redBriMax]))
#cv2.imwrite('RedMasks/redBriMask.png', redBriMask)

redBricks = np.zeros([studCount,studCount])

#Add nested loops to Bitmask Add two requirements
for rowIndex in range(redBricks.shape[0]):
    for colIndex in range(redBricks.shape [1]):
        if (redHueMask[rowIndex,colIndex] == 255) and (redSatMask[rowIndex,colIndex] == 255) and (redBriMask[rowIndex,colIndex] == 255):
            redBricks[rowIndex,colIndex] = 1

#cv2.imwrite('RedMasks/redBricks.png', redBricks*255)



# Setting ranges, The + or - range from the detected mean from the calibration blocks
blankHueRange = 15
blankSatRange = 60
blankBriRange = 40

blankHueMin = blankCalib[0]-blankHueRange
blankHueMax = blankCalib[0]+blankHueRange
blankHueMask = cv2.inRange(hsvImg, np.array([blankHueMin,0,0]), np.array([blankHueMax,255,255]))
#cv2.imwrite('BlankMasks/blankHueMask.png', blankHueMask)

blankSatMin = blankCalib[1]-blankSatRange
blankSatMax = blankCalib[1]+blankSatRange
blankSatMask = cv2.inRange(hsvImg, np.array([0,blankSatMin,0]), np.array([180,blankSatMax,255]))
#cv2.imwrite('BlankMasks/blankSatMask.png', blankSatMask)

blankBriMin = blankCalib[2]-blankBriRange
blankBriMax = blankCalib[2]+blankBriRange
blankBriMask = cv2.inRange(hsvImg, np.array([0,0,blankBriMin]), np.array([180,255,blankBriMax]))
#cv2.imwrite('BlankMasks/blankBriMask.png', blankBriMask)

blankBricks = np.zeros([studCount,studCount])

for rowIndex in range(blankBricks.shape[0]):
    for colIndex in range(blankBricks.shape [1]):
        if (blankHueMask[rowIndex,colIndex] == 255) and (blankSatMask[rowIndex,colIndex] == 255) and (blankBriMask[rowIndex,colIndex] == 255):
            blankBricks[rowIndex,colIndex] = 1

#cv2.imwrite('BlankMasks/blankBricks.png', blankBricks*255)





# The final stud array containing the different colours at each stud
# 0 is unassigned, 1=Green, 2=Blue, 3=Yellow, 4=Red, 5=error, 6=blank
studArray = np.zeros([studCount,studCount])
for rowIndex in range(studArray.shape[0]):
    for colIndex in range(studArray.shape [1]):
        if (greenBricks[rowIndex,colIndex]+blueBricks[rowIndex,colIndex]+yellowBricks[rowIndex,colIndex]+redBricks[rowIndex,colIndex] + blankBricks[rowIndex,colIndex]>1):
            print("ERROR: overalapping colours at row{} col {}. Colours detected at this position green{}, blue{}, yellow{}, red{}, blank{}.".format(rowIndex,colIndex,greenBricks[rowIndex,colIndex],blueBricks[rowIndex,colIndex],yellowBricks[rowIndex,colIndex],redBricks[rowIndex,colIndex],blankBricks[rowIndex,colIndex]))
            studArray[rowIndex,colIndex] = 5
        elif (greenBricks[rowIndex,colIndex]==1):
            studArray[rowIndex,colIndex] = 1
        elif (blueBricks[rowIndex,colIndex]==1):
            studArray[rowIndex,colIndex] = 2
        elif (yellowBricks[rowIndex,colIndex]==1):
            studArray[rowIndex,colIndex]= 3
        elif (redBricks[rowIndex,colIndex]==1):
            studArray[rowIndex,colIndex] = 4
        elif (blankBricks[rowIndex,colIndex]==1):
            studArray[rowIndex,colIndex] = 6

end = timer()
print(end - start) # Time in seconds, e.g. 5.38091952400282

unassigned = np.uint8([0,0,0 ])
green = np.uint8([77,175,0 ])
blue = np.uint8([183,108,0 ])
yellow = np.uint8([0,205,255 ])
red = np.uint8([33,26,221 ])
white = np.uint8([244,244,244 ])
error = np.uint8([0,69,255 ])

# Convert stud array to image for processing
studVisArray = np.zeros([studCount,studCount,3],'uint8')
for rowIndex in range(studVisArray.shape[0]):
    for colIndex in range(studVisArray.shape [1]):
        if studArray[rowIndex,colIndex] == 6:
            studVisArray[rowIndex,colIndex] = white
        elif studArray[rowIndex,colIndex] == 1:
            studVisArray[rowIndex,colIndex] = green
        elif studArray[rowIndex,colIndex] == 2:
            studVisArray[rowIndex,colIndex] = blue
        elif studArray[rowIndex,colIndex] == 3:
            studVisArray[rowIndex,colIndex] = yellow
        elif studArray[rowIndex,colIndex] == 4:
            studVisArray[rowIndex,colIndex] = red
        elif studArray[rowIndex,colIndex] == 0:
            studVisArray[rowIndex,colIndex] = unassigned
        else:
            studVisArray[rowIndex,colIndex] = error

cv2.imwrite('Studs/studsVisulisation.png', studVisArray)




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