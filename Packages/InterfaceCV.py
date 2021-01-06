# Everying needed to obtain a build plate configuration from an image
import numpy as np
import cv2

class BuildPlateComprehension:
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
    def getPlateConfig(self, image, studDimensions):
        plateConfig = False
        
        return plateConfig

    # Provided an HSV image this function returns a list of regions descirbing blobs of different colours in the image. Stud dimensions rows cols
    def getRegions(self, HSVImage, colorRef,studDimensions):
        regions = []

        # Stored as list of coordinates eg [[0,0],[3,4],...]
        visitedStuds = np.zeros(studDimensions)

        # Go though all studes and performa region search
        for row in range (visitedStuds.shape[0]):
            for col in range (visitedStuds.shape[1]):
                if (visitedStuds[row,col] == 0):
                    regions.append(self.regionSearch(row,col,HSVImage,visitedStuds,studDimensions,(5,30,10)))

        return regions

    def regionSearch(self,row,col,HSVImage,visitedStuds,studDimensions, HSVBounds):
        regionAdditions = [(row,col)]
        visitedStuds[row,col] = 1 
        myHSV = HSVImage[row,col]
        
        for p in [[row+1,col],[row,col+1],[row-1,col],[row,col-1]]:
            
            # Check that cord exisits
            if ((0<=p[0]<studDimensions[0]) and (0<=p[1]<studDimensions[1])):
                
                # Check if not visites
                if (visitedStuds[p[0],p[1]] == 0):

                    if (myHSV[0]-HSVBounds[0] < HSVImage[p[0],p[1],0] < myHSV[0]+HSVBounds[0]):
                        if (myHSV[1]-HSVBounds[1] < HSVImage[p[0],p[1],1] < myHSV[1]+HSVBounds[1]):
                            if (myHSV[2]-HSVBounds[2] < HSVImage[p[0],p[1],2] < myHSV[2]+HSVBounds[2]):
                                regionAdditions.extend(self.regionSearch(p[0],p[1],HSVImage,visitedStuds,(studDimensions[0],studDimensions[1]), HSVBounds))
        
        return (regionAdditions)

    def processRegion(self, regions, hSVImage):
        # Formats the list of regions into a region Dictionary

        # Stored as list of dictionaries in format. regions = [region,region,...] where
        # region ={
        #   "region Id": 1
        #   "average HSV": [124,233,68]
        #   "color": "Unknown"
        #   "studs": [[0,0],[1,1]],[[2,3],[4,1]]
        # }

        return

    # Updates the colour estimation of regions within a dictionary based of the inputed colour ref
    def updateColourEstimates(self, regionDictionary, colorRef):
        return

    # Given a dictionary this function returns an 2d array representing the stud configuration, (stud dimensions row,cols)
    def getStudConfigurationFromRegion(self, regionDictionary,studDimensions):
        return