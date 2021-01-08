# Everying needed to obtain a build plate configuration from an image
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

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
        pt1 = np.float32([topLeft,topRight,bottomLeft,bottomRight])

        # Set height and width of final image
        pt2 = np.float32([[0,0],[outputDimensions[0],0],[0,outputDimensions[1]],[outputDimensions[0], outputDimensions[1]]])

        matrix = cv2.getPerspectiveTransform(pt1, pt2)
        warpedImage = cv2.warpPerspective(image, matrix, (outputDimensions[0], outputDimensions[1]))

        return (warpedImage)





    # Input a numpy array based image that has been cropped to the edges of the build plate, outputs the plate config
    def getPlateConfig(self, hsvImage, resisedBGRImage, buildPlateDimensions, hSVRegionAcceptence, colourCalibRef, studColourIDMappings, cIDtoBGR, debugImageDataFilePath, showDebug=False):        
        # hSVRegionAcceptence: a tuple containing the acceptable H,S and V ranges for region formation
        # Colour calib reference: A list of dictionaries for each stud type containing the ID, Average HSV value and the acceptable HSV range
        # Stud Colour ID Mapping: A dictionary where the key is the stud ID and value is a string describing what that stud is
        
        
        regions = self.getRegions(hsvImage,False,buildPlateDimensions,hSVRegionAcceptence)

        regionList = self.processRegion(regions,hsvImage)

        self.updateColourEstimates(regionList,colourCalibRef)
        if (showDebug == True): self.getRegionVisual(regionList,resisedBGRImage,buildPlateDimensions, str(debugImageDataFilePath),studColourIDMappings)

        studConfiguration = self.getStudConfigurationFromRegions(regionList,buildPlateDimensions)
        if (showDebug == True): self.makeStudConfigVisual(studConfiguration,cIDtoBGR, str(debugImageDataFilePath))

        return (studConfiguration)






    # Provided an HSV image this function returns a list of regions descirbing blobs of different colours in the image. Stud dimensions rows cols
    # Bounds are the ranges for the hue, saturation and value need to be withing to be added to a region
    def getRegions(self, HSVImage, colorRef,studDimensions, HSVBounds=(10,10,10)):
        regions = []

        # Stored as list of coordinates eg [[0,0],[3,4],...]
        visitedStuds = np.zeros(studDimensions)

        # Go though all studes and performa region search
        for row in range (visitedStuds.shape[0]):
            for col in range (visitedStuds.shape[1]):
                if (visitedStuds[row,col] == 0):
                    regions.append(self.regionSearch(row,col,HSVImage,visitedStuds,studDimensions,HSVBounds))

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
                "colorID": '0',
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
                if (colorRef[c]['hsv'][1]-colorRef[c]['hsvRange'][1] < region['averageHSV'][1] < colorRef[c]['hsv'][1]+colorRef[c]['hsvRange'][1]):
                    
                    #Check if value in range
                    if (colorRef[c]['hsv'][2]-colorRef[c]['hsvRange'][2] < region['averageHSV'][2] < colorRef[c]['hsv'][2]+colorRef[c]['hsvRange'][2]):
                        
                        #Check if need to loop for hue
                        # Since hue loops back to 0 when it reaches 180 we may need to perform two checks
                        lowerBoundHue = colorRef[c]['hsv'][0]-colorRef[c]['hsvRange'][0]
                        upperBoundHue = colorRef[c]['hsv'][0]+colorRef[c]['hsvRange'][0]
                        
                        # The max value for hue is 180, if the upperbound is greater than 180 we need to perform an additional chack
                        # between 0 and the upper bound -180
                        if (upperBoundHue >180):
                            if (lowerBoundHue < region['averageHSV'][0]) or (region['averageHSV'][0] < upperBoundHue-180):
                                region['colorID'] = c
                                break

                        # Th opposite can also occur when starting with a very 
                        elif (lowerBoundHue < 0):
                            if (lowerBoundHue+180 < region['averageHSV'][0]) or (region['averageHSV'][0] < upperBoundHue):
                                region['colorID'] = c
                                break

                        else: # region does not overstep range, performa regular check
                            if (lowerBoundHue < region['averageHSV'][0] < upperBoundHue):                            
                                region['colorID'] = c
                                break
        return

    # Creates a debuggin visual of all the regions as a map
    def getRegionVisual(self, regionListDictionary, scaledImage, studDimensions, filePath, colourIDMap, imScale=150,):
        imageDimensions = (studDimensions[0]*imScale,studDimensions[1]*imScale)
        
        # Visulisation
        upscaledResizedImg = cv2.resize(scaledImage, imageDimensions, interpolation=cv2.INTER_AREA)

        cv2.imwrite(filePath + 'upscaledResizedImg.png', upscaledResizedImg)

        visImg = Image.open(filePath + 'upscaledResizedImg.png')

        my_dpi=100

        # Hue Figure
        hueFig=plt.figure(figsize=(float(visImg.size[0])/my_dpi,float(visImg.size[1])/my_dpi),dpi=my_dpi)
        ax=hueFig.add_subplot(111)

        # Set the gridding interval: here we use the major tick interval
        myInterval=imageDimensions[0]/studDimensions[0]
        loc = plticker.MultipleLocator(base=myInterval)
        ax.xaxis.set_major_locator(loc)
        ax.yaxis.set_major_locator(loc)

        # Add the grid
        ax.grid(which='major', axis='both', linestyle='-', color='g')

        # Add the image
        ax.imshow(visImg)

        for region in regionListDictionary:
            ax.text(region['studs'][0][1]*myInterval, region['studs'][0][0]*myInterval+60, str(region['averageHSV'][0]))
            ax.text(region['studs'][0][1]*myInterval, region['studs'][0][0]*myInterval+80, str(region['averageHSV'][1]))
            ax.text(region['studs'][0][1]*myInterval, region['studs'][0][0]*myInterval+100, str(region['averageHSV'][2]))

            for stud in region['studs']:
                ax.text(stud[1]*myInterval,stud[0]*myInterval+35,region['regionId'], fontsize=25)
                
                colourType = colourIDMap[region['colorID']]
                ax.text(stud[1]*myInterval,stud[0]*myInterval+130, colourType)


        # Save the figure
        hueFig.suptitle('Region Map', fontsize=16)
        hueFig.savefig(filePath + 'RegionMapVisulisation.png')
        return

    # Given a dictionary this function returns an 2d array representing the stud configuration, (stud dimensions row,cols)
    def getStudConfigurationFromRegions(self, regionDictionary,studDimensions):
        studConfiguration = np.zeros((studDimensions[0],studDimensions[1]))
        
        for region in regionDictionary:
            for stud in region['studs']:
                studConfiguration[stud[0],stud[1]] = int(region['colorID'])

        return (studConfiguration)

    def makeStudConfigVisual(self, studConfig, colourIdtoVis, filePath):
        # Convert stud array to image for processing
        studVisArray = np.zeros([studConfig.shape[0],studConfig.shape[1],3],dtype=int)
        for rowIndex in range(studConfig.shape[0]):
            for colIndex in range(studConfig.shape [1]):
                    studVisArray[rowIndex,colIndex] = colourIdtoVis[studConfig[rowIndex,colIndex]]
                

        cv2.imwrite(filePath + 'studConfigVisulisation.png', studVisArray)

    def getCalibration(self, hsVImage, calibrationMap):
        if (hsVImage.shape[0] != calibrationMap.shape[0]) or (hsVImage.shape[1] != calibrationMap.shape[1]):
            print ('Calibration map and hsvImage are of different dimension')
            return

        colourCalib ={
            #key of dictionary is the colour id:{
            # hsv
            # hsvRange
            # }
        }
        
        # Retain hsv and hsv range for old methods of colour recognition
        for row in range (calibrationMap.shape[0]):
            for col in range (calibrationMap.shape[1]):
                hsvValues = hsVImage[row,col]


                if (calibrationMap[row,col] in colourCalib):           
                    colourCalib[calibrationMap[row,col]]['visitedCords'] = np.append(colourCalib[calibrationMap[row,col]]['visitedCords'],[[row,col]],0)
                
                else:
                    colourCalib[calibrationMap[row,col]] ={
                        'hsv': (0,0,0), # HSV of colour in photos
                        'hsvRange':(20,70,40), # HSV ranges for acceptance
                        
                        # Used for calculateion
                        'visitedCords': np.array([[row,col]])
                    }

        # For each colour if in the colour calib
        for key in colourCalib:
            avgHSV = self.calcAvgHSV (colourCalib[key]['visitedCords'], hsVImage)
            colourCalib[key]['hsv'] = avgHSV 



        # Calculate range
        for key in colourCalib:
            # Key is the colour ID
            minMaxVals = self.getMinAndMaxHSV(hsVImage,colourCalib[key]['visitedCords'])


            colourCalib[key]['minH'] = minMaxVals[0]
            colourCalib[key]['minS'] = minMaxVals[1]
            colourCalib[key]['minV'] = minMaxVals[2]

            colourCalib[key]['maxH'] = minMaxVals[3]
            colourCalib[key]['maxS'] = minMaxVals[4]
            colourCalib[key]['maxV'] = minMaxVals[5]


        for key in colourCalib:
            colourCalib[key].pop('visitedCords', None)
                

        return(colourCalib)

    # Given and hsv image and a list of coordinates returns the min and max hsv values as a list
    # Returned values format [minH, minS, minV, maxH, maxS, maxV]
    def getMinAndMaxHSV(self, hsvImage, coords):
        minH = float('inf')
        minS = float('inf')
        minV = float('inf')
        maxH = float('-inf')
        maxS = float('-inf')
        maxV = float('-inf')

        for cord in coords:
            if (hsvImage[cord[0],cord[1],0]<minH): minH = hsvImage[cord[0],cord[1],0]
            if (hsvImage[cord[0],cord[1],1]<minS): minS = hsvImage[cord[0],cord[1],1]
            if (hsvImage[cord[0],cord[1],2]<minV): minV = hsvImage[cord[0],cord[1],2]

            if (hsvImage[cord[0],cord[1],0]>maxH): maxH = hsvImage[cord[0],cord[1],0]
            if (hsvImage[cord[0],cord[1],1]>maxS): maxS = hsvImage[cord[0],cord[1],1]
            if (hsvImage[cord[0],cord[1],2]>maxV): maxV = hsvImage[cord[0],cord[1],2]

        # Looping check
        if (maxH-minH > 90):
            # Perform looping changes needed
            oldMin = minH
            minH = maxH
            
            maxH = oldMin + 180
            

        return([minH, minS, minV, maxH, maxS, maxV])