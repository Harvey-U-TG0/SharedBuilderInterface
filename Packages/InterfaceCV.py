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
                    if (myHSV[1]-HSVBounds[1] < HSVImage[p[0],p[1],1] < myHSV[1]+HSVBounds[1]): #Saturation Check
                        if (myHSV[2]-HSVBounds[2] < HSVImage[p[0],p[1],2] < myHSV[2]+HSVBounds[2]): #Value Check
                            
                            # Since hue loops back to 0 when it reaches 180 we may need to perform two checks
                            lowerBoundHue = myHSV[0]-HSVBounds[0]
                            upperBoundHue = myHSV[0]+HSVBounds[0]
                            
                            # The max value for hue is 180, if the upperbound is greater than 180 we need to perform an additional chack
                            # between 0 and the upper bound -180
                            if (upperBoundHue >180):
                                if (lowerBoundHue < HSVImage[p[0],p[1],0]) or (HSVImage[p[0],p[1],0] < upperBoundHue-180):
                                    regionAdditions.extend(self.regionSearch(p[0],p[1],HSVImage,visitedStuds,(studDimensions[0],studDimensions[1]), HSVBounds))
                            # Th opposite can also occur when starting with a very 
                            elif (lowerBoundHue < 0):
                                if (lowerBoundHue+180 < HSVImage[p[0],p[1],0]) or (HSVImage[p[0],p[1],0] < upperBoundHue):
                                    regionAdditions.extend(self.regionSearch(p[0],p[1],HSVImage,visitedStuds,(studDimensions[0],studDimensions[1]), HSVBounds))

                            else: # region does not overstep range, performa regular check
                                if (myHSV[0]-HSVBounds[0] < HSVImage[p[0],p[1],0] < myHSV[0]+HSVBounds[0]):                            
                                    regionAdditions.extend(self.regionSearch(p[0],p[1],HSVImage,visitedStuds,(studDimensions[0],studDimensions[1]), HSVBounds))
        
        return (regionAdditions)


    # Formats the list of regions into a region Dictionary
    def processRegion(self, regions, hSVImage):
        newId = 0
        regionList = [] # List of dicts
        
        for region in regions:
            # Calculate average for HSV values

            regionDict ={
                "regionId": newId,
                "averageHSV": self.calcAvgHSV(region,hSVImage),
                "color": "Unknown",
                "studs": region
            }

            regionList.append(regionDict)

            newId += 1
        return (regionList)

    #Given a list of (row,col) coordinates and an HSV image returns the average HSV value
    def calcAvgHSV (self, region, hsvImage):       
        # Check if looping is needed
        # If the the difference between the smallest and greatest hue is greater than 90 then add 180 to all values below 90
        # If the mean at the end is greatr than 180, subtract 180
        hueLoop = False
        minHue = 90
        maxHue = 90
        for cordinate in region:
            if (hsvImage[cordinate[0],cordinate[1],0]<minHue):
                minHue = hsvImage[cordinate[0],cordinate[1],0]
            elif (hsvImage[cordinate[0],cordinate[1],0]>maxHue):
                maxHue = hsvImage[cordinate[0],cordinate[1],0]
        
        if ((maxHue - minHue) > 90):
            hueLoop = True
        
        hueTot = 0
        satTot = 0
        valTot = 0
        for cordinate in region:
            hueValue = hsvImage[cordinate[0],cordinate[1],0]
            
            if (hueLoop) and (hueValue<90):
                hueValue += 180
                print(hueValue)

            hueTot += hueValue
            satTot += hsvImage[cordinate[0],cordinate[1],1]
            valTot += hsvImage[cordinate[0],cordinate[1],2]

        hueAvg = hueTot/len(region)
        if (hueAvg >180): hueAvg-=180
        satAvg = satTot/len(region)
        valAvg = valTot/len(region)

        return(np.array([hueAvg,satAvg,valAvg]))

    # Updates the colour estimation of regions within a dictionary based of the inputed colour ref
    def updateColourEstimates(self, regionListDictionary, colorRef):
        for region in regionListDictionary:
            for c in colorRef:
                # Check if saturation in range
                if (c['hsv'][1]-c['hsvRange'][1] < region['averageHSV'][1] < c['hsv'][1]+c['hsvRange'][1]):
                    
                    #Check if value in range
                    if (c['hsv'][2]-c['hsvRange'][2] < region['averageHSV'][2] < c['hsv'][2]+c['hsvRange'][2]):
                        
                        #Check if need to loop for hue
                        # Since hue loops back to 0 when it reaches 180 we may need to perform two checks
                        lowerBoundHue = c['hsv'][0]-c['hsvRange'][0]
                        upperBoundHue = c['hsv'][0]+c['hsvRange'][0]
                        
                        # The max value for hue is 180, if the upperbound is greater than 180 we need to perform an additional chack
                        # between 0 and the upper bound -180
                        if (upperBoundHue >180):
                            if (lowerBoundHue < region['averageHSV'][0]) or (region['averageHSV'][0] < upperBoundHue-180):
                                region['color'] = c['colour']
                                break

                        # Th opposite can also occur when starting with a very 
                        elif (lowerBoundHue < 0):
                            if (lowerBoundHue+180 < region['averageHSV'][0]) or (region['averageHSV'][0] < upperBoundHue):
                                region['color'] = c['colour']
                                break

                        else: # region does not overstep range, performa regular check
                            if (lowerBoundHue < region['averageHSV'][0] < upperBoundHue):                            
                                region['color'] = c['colour']
                                break
        return

    # Creates a debuggin visual of all the regions as a map
    def getRegionVisual(self, regionDictionary):
        return

    # Given a dictionary this function returns an 2d array representing the stud configuration, (stud dimensions row,cols)
    def getStudConfigurationFromRegion(self, regionDictionary,studDimensions):
        return