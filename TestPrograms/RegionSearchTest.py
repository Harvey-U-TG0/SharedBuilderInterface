
import cv2
import numpy as np

import sys
sys.path.append('/home/pi/Git/SharedBuilderInterface/Packages')
sys.path.append('/home/pi/Git/SharedBuilderInterface/TestData')

from InterfaceCV import BuildPlateComprehension

# Create build plate comprehension object
cVObject = BuildPlateComprehension()

studCount = 24

img = cv2.imread('ImageData/Test/warped.png')

# Resize Image
resizedImg = cv2.resize(img, (24,24), interpolation=cv2.INTER_AREA)
#cv2.imwrite('images/resizedImg.png', resizedImg)

# Convert to HSV
hsvImg = cv2.cvtColor(resizedImg,cv2.COLOR_BGR2HSV)

visitedStuds = np.zeros((studCount,studCount))
region=cVObject.regionSearch(1,7,hsvImg,visitedStuds,(studCount,studCount),(5,30,10))


regions = cVObject.getRegions(hsvImg,False,(studCount,studCount))


Average = cVObject.calcAvgHSV(regions[12],hsvImg)
print (regions[12])
print (Average)