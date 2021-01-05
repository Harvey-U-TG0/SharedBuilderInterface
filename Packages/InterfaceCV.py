# Everying needed to obtain a build plate configuration from an image
class BuildPlateComprehension:
    import numpy as np
    import cv2


    defaultCorners = np.array([[0,0],[1,0],[1,1],[0,1]])


    def warpToBuildPlate(self,image):
        cornerCords = self.getBuildPlateCorners(image)
        warpedImage = self.warpToBuildPlateFromCords(image,cornerCords)
        return warpedImage

    # Input an image and 
    def getBuildPlateCorners(self, image):
        raise Exception("Automatic detection of corners not yet implemented, use from cords manually instead")
        # To Do: Implement automatic detection of corners if needed

    # Outputs an image (as numpy array) by warping an input image based of the supplied corner coordinates
    def warpToBuildPlateFromCords(self,image, cornerCords=defaultCorners, outputDimensions = [480,480]):
        if (cornerCords.shape != (4, 2)):
            raise Exception("Incorrect shape corner coorsinates must be of shape (4,2)")

        #Corner Coordinates
        topLeft = cornerCords[0]
        topRight = cornerCords[1]
        bottomLeft = cornerCords[2]
        bottomRight = cornerCords[3]

        # Input warp
        pt1 = self.np.float32([topLeft,topRight,bottomLeft,bottomRight])

        # Set height and width of final image
        pt2 = self.np.float32([[0,0],[outputDimensions[0],0],[0,outputDimensions[1]],[outputDimensions[0], outputDimensions[1]]])

        matrix = self.cv2.getPerspectiveTransform(pt1, pt2)
        warpedImage = self.cv2.warpPerspective(image, matrix, (outputDimensions[0], outputDimensions[1]))

        return (warpedImage)


    # Input a numpy array based image that has been cropped to the edges of the build plate, outputs the plate config
    def getPlateConfig(self, image, studCount):
        plateConfig = False
        
        return plateConfig