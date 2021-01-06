import sys
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
sys.path.append('/home/pi/Git/SharedBuilderInterface/Packages')
sys.path.append('/home/pi/Git/SharedBuilderInterface/TestData')

from API import InterfaceAPI
from testData import ITestData

# Create an InterfaceAPI object that will be used for server communications
interface = InterfaceAPI('http://192.168.1.73:5000/','Emily')

interface.postData(ITestData.arrangementA)
