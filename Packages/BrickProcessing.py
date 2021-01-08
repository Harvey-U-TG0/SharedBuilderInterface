# Everying needed to obtain a build plate configuration from an image
import numpy as np
import cv2

import sys
sys.path.append('/home/pi/Git/SharedBuilderInterface/Data')

from Data import appData

class BrickComprehension:
    
    # Given an exisiting brick config, uses data from a new stud config to output an up to data brick config
    # Brick configuration data is provided as a list of brick dictionaries
    # Stud configuration is provided as a (studxstud) numpy array where number represents the stud state
    def updateBrickConfig(self, oldBrickConfig, newStudConfig):
        # Get map of understood studs

        # Remove bricks if possible

        # Add bricks if possible

        return

    # Given a stud configuration, this function outputs an array of the same dimension
    # where 1 represents locations that can be used to inform brick understanding
    # studnullid is the value in the stud config that represents an unknown stud
    def generateUsabilityMap(self, studConfig, studNullId = 0):
        usabilityMap = np.ones((studConfig.shape[0],studConfig.shape[1]))

        # Kernal for a region to satisfiy if not usable, essentially only regions of more than 2x2 unkown cannot be used
        # as this stops shadows from preventing updates
        regKernal = np.array([[0,0],[0,1],[1,0],[1,1]])

        kernalHeight = 0
        for element in regKernal:
            if (element[0]>kernalHeight): kernalHeight = element[0]

        kernalWidth = 0
        for element in regKernal:
            if (element[1]>kernalWidth): kernalWidth = element[1]

        # The array put onto the places where the reg kernal is detected. Larger to help fill in the blobs
        outputKernal = np.array([[-1,-1],[-1,0],[-1,1],[-1,2],      
                                 [0,-1],[0,0],[0,1],[0,2],
                                 [1,-1],[1,0],[1,1],[1,2],
                                 [2,-1],[2,0],[2,1],[2,2]])

        for row in range (studConfig.shape[0]-kernalHeight):
            for col in range (studConfig.shape[1]-kernalWidth):
                # at a cordinate
                usable = False
                for element in regKernal:
                    if (studConfig[row+element[0],col+element[1]] != studNullId):
                        usable = True
                        break

                if (usable == False):
                    # Add output kernal to usabilit map    
                    for element in outputKernal:
                        position = np.array([row+element[0],col+element[1]])
                        
                        # Check if the desired coordinate is in the usability map
                        if (0<position[0]<usabilityMap.shape[0]) and (0<position[1]<usabilityMap.shape[1]):
                            # If so set that position on the usability map to 0
                            usabilityMap[position[0],position[1]] = 0

        return (usabilityMap)
    
    # Outputs a new brick config with bricks removed if indicated by the stud configuration
    # Operates where usability map indicates useful data can be obtained
    def removeBricks(self, studConfig, usabilityMap, brickConfig):
        bricksToRemove = []

        for brick in brickConfig:
            # From the starting position check ever stud in the brick(as long as it is usable) if any of them are not the correct ID then delete it
            shapeID = brick['shapeID']
            colourID = brick['colourID']
            position = brick['position']

            # Get the list of studs for that brick id
            studs = appData.bricksRef[shapeID]['shape']

            keep = True
            for stud in studs:
                # Get the coordinate of that tile
                studAbsolute = (position[0]+stud[0], position[1]+stud[1])

                # Check if that coordinate is in the usability map
                if usabilityMap[studAbsolute[0],studAbsolute[1]] == 1:
                    
                    # If so then check if that studs id colour is corect
                    if (studConfig[studAbsolute[0],studAbsolute[1]] != colourID):
                        keep = False;
                else:
                    keep=True
                    break

            if (keep == False):
                bricksToRemove.append(brick)
            
        for brick in bricksToRemove:
            brickConfig.remove(brick)
            print('Removed brick '+ str(brick))

        # Note, the origianl brick config is also changed
        return (brickConfig)



    # Given the latest stud config and a brick config, this function adds bricks to to brick congif list
    # Bricks ref pro is a bricks ref also containing the brick outlines
    # valid brick colours sepcifies the lower and upper bounds for stud ids the corespond to bricks (both inclusive)
    def addBricks(self, studConfig, usabilityMap, brickConfig, bricksRefPro, validBrickColourIds=(6,15), debug = False):
        # We want to ignore studs that are part of a brick already
        # Make a new array of studs accounted for by bricks
        usedUpMap = self.generateUsedUpMap(brickConfig,bricksRefPro,studConfig.shape)
    
        # Go through all the remaining studs in the stud config that are usable and not in the brick accounted for array
        for row in range (studConfig.shape[0]):
            for col in range (studConfig.shape[1]):
                if (usabilityMap[row,col] == 1) and (usedUpMap[row,col] == 1):
                    # we can use this brick, next check if the id of this stud is useful
                        studColID = studConfig[row,col]
                        if (validBrickColourIds[0]<= studColID <= validBrickColourIds[1]):
                            # There is a coloured stud here
                            for key in bricksRefPro:
                                potentialBrick = bricksRefPro[key]
                                
                                
                                shapeStudsMatch = True
                                # Check if all shape studs match
                                for stud in potentialBrick['shape']:
                                    rowPos = row+stud[0]
                                    colPos = col+stud[1]

                                    #Check if the stud exists on the build plate, if not then reject the brick
                                    if (0> rowPos) or (studConfig.shape[0]<= rowPos) or (0> colPos) or (studConfig.shape[1]<= colPos):
                                        shapeStudsMatch = False
                                        if (debug==True): print('Exited due to stud no on plate')
                                        break

                                    # If the stud is a different colour, not usable or already used up reject this possiblity
                                    if (studConfig[rowPos,colPos] != studColID):
                                        shapeStudsMatch = False
                                        if (debug==True): print('Exited due to stud not matching')
                                        break
                                        # Stud doesnt match, reject this potential brick

                                    if (usabilityMap[rowPos,colPos] == 0):
                                        shapeStudsMatch = False
                                        if (debug==True): print('Exited usability map of that stud is 0')
                                        break

                                    if (usedUpMap[rowPos, colPos]==0):
                                        shapeStudsMatch = False
                                        if (debug==True): print('Exited due to that stud already being used')
                                        break


                                # If all the shape studs match, the perform additional checks on the outline studs
                                if (shapeStudsMatch == True):
                                    for stud in potentialBrick['shapeOutline']:
                                        rowPos = row+stud[0]
                                        colPos = col+stud[1]
                                        
                                        # If that stud exists
                                        if (0<= rowPos) and (studConfig.shape[0]> rowPos) and (0<= colPos) and (studConfig.shape[1]> colPos):
                                            if (usabilityMap[rowPos,colPos] == 0):
                                                shapeStudsMatch =False
                                                if (debug==True): print('Exited due to outline brick not being usable')
                                                break
                                    
                                            if ((studConfig[rowPos,colPos] == studColID) and (usedUpMap[rowPos,colPos] == 1)):
                                                shapeStudsMatch = False
                                                if (debug==True): print('Exited due to extra brick available')
                                                break

                                if (shapeStudsMatch ==True):
                                    # Add this brick to the dictionary 
                                    brickConfig.append({
                                        'shapeID': key,
                                        "position": [row,col],
                                        "colourID": studColID
                                    })



                                    print('added brick')
                                    break


        # If get to one that is not unknown or not a build plate
            # Test each brick kernal
                # If there is an exact match then add brick to the brick config

        return (brickConfig) 
    
    
    # Provided with a bricks reference dictionary, this function adds brick outline section for each brick
    # Note: modifies the original bricksRef dictionary inputed
    def generateBrickOutlines(self, bricksRef):
        for key in bricksRef.keys():
            brick = bricksRef[key]
            
            outlineCords = []
            for stud in brick['shape']:
                
                # Check top, left, bottom, right
                for position in [((stud[0]), (stud[1]+1)),(stud[0]+1, stud[1]),(stud[0], stud[1]-1),(stud[0]-1, stud[1])]:
                    shouldInclude = True
                    # Check if not in stud array
                    for s in brick['shape']:
                        if np.array_equal(position,s):
                            shouldInclude = False
                            break
                    # if not in stud array then add to outline cords
                    if (shouldInclude == True):
                        outlineCords.append(position)

            brick['shapeOutline'] = outlineCords

        return bricksRef

    # Generates a map of studs that have been (used up) by bricks already in the dictionary. 0 means it has been used up, and can't be used by new bricks
    def generateUsedUpMap(self,brickConfig,bricksRef,studDimensions):
        usedUpMap = np.ones((studDimensions[0],studDimensions[1]))

        for brick in brickConfig:
            shapeID = brick['shapeID']
            print(shapeID)
            brickPosition = brick['position']

            # Get the list of studs for that brick id
            studsOfBrick = bricksRef[shapeID]['shape']

            for stud in studsOfBrick:
                position = np.array([stud[0]+brickPosition[0],stud[1]+brickPosition[1]])
                print(position)
                usedUpMap[position[0],position[1]] = 0


        return (usedUpMap)