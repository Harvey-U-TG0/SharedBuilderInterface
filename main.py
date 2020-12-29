from time import sleep
import numpy as np
from picamera import PiCamera
import cv2

# Take photo


#with PiCamera() as camera:
#    camera.resolution = (2592, 1944)
#    camera.rotation = 0
#    camera.vflip = False
#    camera.hflip = False
#    sleep(2) # Camera warm-up time
#    camera.capture('images/image1.jpg')


# Load image into CV
originalImg = cv2.imread('images/image1.jpg',1)

#originalImg = cv2.resize(originalImga, (480,480), interpolation=cv2.INTER_AREA)

# Make image grayscale
#grayImg = cv2.cvtColor(originalImg, cv2.COLOR_BGR2GRAY)
#grayImg = originalImg

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
resizedImg = cv2.resize(warpedImg, (24,24), interpolation=cv2.INTER_AREA)
cv2.imwrite('images/resizedImg.png', resizedImg)

# Convert to HSV
hsvImg = cv2.cvtColor(resizedImg,cv2.COLOR_BGR2HSV)

print (hsvImg[0,0])

edges = cv2.Canny(warpedImg,10,200)
cv2.imwrite('images/edgy.jpg', edges)


thresholdA = 50
#warpedThresholdImg = cv2.adaptiveThreshold(warpedImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 1)
ret, warpedThresholdImg = cv2.threshold(warpedImg,thresholdA,255,cv2.THRESH_BINARY)
cv2.imwrite('images/warpedThresholdImg.jpg', warpedThresholdImg)

kernal = np.ones((5,5),'uint8')

# Erode to make sure bricks filled in
erodedImg = cv2.erode(warpedThresholdImg,kernal,iterations=1)
cv2.imwrite('images/erodedImg.jpg', erodedImg)


# Dilation (less black) to get rid of studs
dilatedImg = cv2.dilate(erodedImg,kernal,iterations=3)
cv2.imwrite('images/dilatedImg.jpg', dilatedImg)

# Resize Image
#resizedImg = cv2.resize(dilatedImg, (48,48), interpolation=cv2.INTER_AREA)
#cv2.imwrite('images/resizedImg.png', resizedImg)

# Simple thresholding
threshold = 200
ret, thresholdImg = cv2.threshold(resizedImg,threshold,255,cv2.THRESH_BINARY)
#thresholdImg = cv2.adaptiveThreshold(resizedImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 131, 1)
cv2.imwrite('images/thresholdImg.png', thresholdImg)

print(thresholdImg.shape)

# Custom stud testing
# Make a new empty array of dimensions 
#brickArray = np.zeros([24,24], dtype='uint8')
#for rowIndex in range (brickArray.shape[0]):
#    for colIndex in range (brickArray.shape [1]):
#        totalBlack = 0
#        if thresholdImg[rowIndex*2,colIndex*2] == 0:
#            totalBlack += 1
#        if thresholdImg[rowIndex*2+1,colIndex*2] == 0:
#            totalBlack += 1
#        if thresholdImg[rowIndex*2,colIndex*2+1] == 0:
#            totalBlack += 1
#        if thresholdImg[rowIndex*2+1,colIndex*2+1] == 0:
#            totalBlack += 1
#        
#        if (totalBlack >=4):
#            brickArray[rowIndex,colIndex] = 255

#cv2.imwrite('images/brickArray.png', brickArray)


# Make that array into image




# Blob it
#thres_adapt = cv2.adaptiveThreshold(output, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)



#cv2.imwrite('AdaptiveThres.bmp',thres_adapt)

#Grid it depending on number of pixels