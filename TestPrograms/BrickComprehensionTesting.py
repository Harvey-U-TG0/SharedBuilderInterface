import sys
sys.path.append('/home/pi/Git/SharedBuilderInterface/Packages')
sys.path.append('/home/pi/Git/SharedBuilderInterface/TestData')

from testData import StudConfigTestData
from BrickProcessing import BrickComprehension


brickProcessor = BrickComprehension()

studConfig = StudConfigTestData.studConfigA

usabilityMap = brickProcessor.generateUsabilityMap(studConfig)

print (usabilityMap)