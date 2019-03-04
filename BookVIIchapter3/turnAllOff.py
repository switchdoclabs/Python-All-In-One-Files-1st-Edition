#!/usr/bin/python3
# Robot Interface Test

import RobotInterface 
import time

RI = RobotInterface.RobotInterface()

print ("turn all off and center")

RI.centerAllServos()
RI.allLEDSOff()





