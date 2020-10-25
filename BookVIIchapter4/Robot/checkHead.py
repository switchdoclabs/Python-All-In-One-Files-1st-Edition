# Zeros Robot


import RobotInterface 
import time

RI = RobotInterface.RobotInterface()


RI.stopMotor()
RI.allLEDSOff()
RI.wheelsMiddle()
RI.headTiltMiddle()
RI.headTurnMiddle()


RI.headTurnPercent(0)
print("HT = 0");
time.sleep(5)
RI.headTurnPercent(100)
print("HT = 100");
time.sleep(5)


RI.wheelsPercent(0)
print("WT = 0");
time.sleep(5)
RI.wheelsPercent(100)
print("WT = 100");
time.sleep(5)
RI.headTiltPercent(0)
print("HT = 0");
time.sleep(5)
RI.headTiltPercent(100)
print("HT = 100");
print




