
import cv2
import numpy as np

import sys
sys.path.append('/home/pi/Git/SharedBuilderInterface/Packages')
sys.path.append('/home/pi/Git/SharedBuilderInterface/TestData')

from InterfaceCV import BuildPlateComprehension

# Create build plate comprehension object
cVObject = BuildPlateComprehension()


img = cv2.imread('ImageData/InputImages/HandTestA.jpeg')

cornerCords = np.array([[343,230],[724,242],[324,616],[719,631]])
warpedImg= cVObject.warpToBuildPlateFromCords(img,cornerCords)

cv2.imwrite('ImageData/Test/warped.png',warpedImg)