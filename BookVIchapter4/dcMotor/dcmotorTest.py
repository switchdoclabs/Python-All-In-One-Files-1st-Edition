
import sys
sys.path.append("./SDL_Pi_GroveI2CMotorDriver")


import SDL_Pi_GroveI2CMotorDriver 
import time

#"0b1010" defines the output polarity 
#"10" means the M+ is "positive" while the M- is "negative"

MOTOR_FORWARD =  0b1010
MOTOR_BACKWARD =  0b0101


try:
	# You can initialize with a different address too: grove_i2c_motor_driver.motor_driver(address=0x0a)
	m= SDL_Pi_GroveI2CMotorDriver.motor_driver()

	#FORWARD
	print("Forward")
        #defines the speed of motor 1 and motor 2;)
	m.MotorSpeedSetAB(100,100)	
        m.MotorDirectionSet(MOTOR_FORWARD)	
	time.sleep(2)

	#BACK
	print("Back")
	m.MotorSpeedSetAB(100,100)
	#0b0101  Rotating in the opposite direction
        m.MotorDirectionSet(MOTOR_BACKWARD)	
	time.sleep(2)

	#STOP
	print("Stop")
	m.MotorSpeedSetAB(0,0)
	time.sleep(1)

	#Increase speed
	for i in range (100):
		print("Speed:",i)
		m.MotorSpeedSetAB(i,i)
		time.sleep(.02)
		
	print("Stop")
	m.MotorSpeedSetAB(0,0)	
	
except IOError:
	print("Unable to find the I2C motor driver")
	print("Hit Reset Button on I2C Motor Driver and Try Again") 

