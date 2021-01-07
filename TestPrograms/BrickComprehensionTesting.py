import sys
sys.path.append('/home/pi/Git/SharedBuilderInterface/Packages')
sys.path.append('/home/pi/Git/SharedBuilderInterface/TestData')
sys.path.append('/home/pi/Git/SharedBuilderInterface/Data')

from testData import StudConfigTestData, BrickConfigTestData
from BrickProcessing import BrickComprehension
from Data import appData


brickProcessor = BrickComprehension()

# Get the latest stud configruation
studConfig = StudConfigTestData.studConfigA
print ('orginal stud configuration')
print(studConfig)
print()

# Get the current brick config
brickConfig = BrickConfigTestData.brickConfigA
print ('orginal brick configuration')
print(brickConfig)
print()

# Generate usability map
usabilityMap = brickProcessor.generateUsabilityMap(studConfig)

print (usabilityMap)



# Remove unneded bricks
brickConfig = brickProcessor.removeBricks(studConfig, usabilityMap, brickConfig)



# Upgrade brick refs with outlines

appData.bricksRef

bricksRef = brickProcessor.generateBrickOutlines(appData.bricksRef)


usedUpMap = brickProcessor.generateUsedUpMap(brickConfig,bricksRef,studConfig.shape)

print (usedUpMap)