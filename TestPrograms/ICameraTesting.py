import sys
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
sys.path.append('/home/pi/Git/SharedBuilderInterface/Packages')
sys.path.append('/home/pi/Git/SharedBuilderInterface/TestData')
import cv2

from ICamera import InterfaceCamera

camera = InterfaceCamera()

cv2.imwrite('ImageData/Test/piCapture.png', camera.getCapture())

