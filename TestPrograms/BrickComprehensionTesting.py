import sys
sys.path.append('/home/pi/Git/SharedBuilderInterface/Packages')
sys.path.append('/home/pi/Git/SharedBuilderInterface/TestData')

from testData import StudConfigTestData, BrickConfigTestData
from BrickProcessing import BrickComprehension


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

print(brickConfig)
