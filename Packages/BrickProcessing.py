# Everying needed to obtain a build plate configuration from an image
import numpy as np
import cv2

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

        # The array put onto the 
        outputKernal = np.array([[0,0],[0,1],[1,0],[1,1])

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
        for brick in brickConfig:
            # From the starting position check ever stud in the brick(as long as it is usable) if any of them are not the correct ID then delete it
            brickID = brick['id']

            # Get the list of studs for that brick id