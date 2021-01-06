
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


regions = cVObject.getRegions(hsvImg,False,(studCount,studCount),(30,30,30))


Average = cVObject.calcAvgHSV(regions[12],hsvImg)
#print (regions[12])
#print (Average)

regionList = cVObject.processRegion(regions,hsvImg)

print (regionList[12])


colourRef=[
    {
        'colour': 'Red', # String name of colour
        'colourID': 1, # ID number for colour
        'hsv': (179,185,150), # HSV of colour in photos
        'hsvRange':(10,10,10), # HSV ranges for acceptance
        'visRGB': np.uint8([0,69,255]) # RGB colour for visulisation purposes
    }
    ]

colourIDMappings = {
    0: 'Null',
    1: 'Red'
}

colourIDtoVis = {
    0: np.uint8([0,0,0]),
    1: np.uint8([0,0,255]) #BGR
}



cVObject.updateColourEstimates(regionList,colourRef)

print (regionList[12])

#cVObject.getRegionVisual(regionList,resizedImg,(studCount,studCount),"ImageData/graphs/",colourIDMappings)

studConfiguration = cVObject.getStudConfigurationFromRegions(regionList,(studCount,studCount))

print (studConfiguration)

cVObject.makeStudConfigVisual(studConfiguration,colourIDtoVis, "ImageData/graphs/" )