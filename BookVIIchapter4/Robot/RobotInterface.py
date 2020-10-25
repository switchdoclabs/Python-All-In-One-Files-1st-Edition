#!/usr/bin/python3
# Robot Interface Wrapper Class
# Version 1.2 Second Edition PAOI
# John C. Shovic, SwitchDoc Labs

DEBUG = True

import RPi.GPIO as GPIO
import motor
import socket
import time
import threading
import led
import os
import ultra

import sys
sys.path.append("./Adafruit_Python_PCA9685/Adafruit_PCA9685")

import PCA9685

import calValues

# LED strip configuration:
LED_COUNT      = 12      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# start up Pixel Strip

from rpi_ws281x import *  
from neopixel  import *

import pixelFunctions 

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()


# set up PWM Pins
pwm = PCA9685.PCA9685()    

class RobotInterface(object):
        # Front RGB LED GPIO Mapping

        left_R = 15
        left_G = 16
        left_B = 18
     
        right_R = 19
        right_G = 21
        right_B = 22
    
        LED_Side_Left = 0
        LED_Side_Right = 1
     
        # main motor constants
        forward    = 1          #Motor forward
        backward   = 0          #Motor backward
     
        left_spd   = 100         #Speed of the car
        right_spd  = 100         #Speed of the car

        MOTOR_START = 1
        MOTOR_STOP = 0
        #servo mapping
        HEAD_TILT_SERVO = 0 # pmw 0 head tilt
        HEAD_TURN_SERVO = 1 # pwm 1 head turn
        WHEELS_TURN_SERVO = 2 # pwm 2 wheels turn

        # color function for pixels

        def Color(self, red, green, blue, white = 0):
            """Convert the provided red, green, blue color to a 24-bit color value.
            Each color component should be a value 0-255 where 0 is the lowest intensity
            and 255 is the highest intensity.
            """
            return (white << 24) | (red << 16)| (green << 8) | blue

        def __init__(self):
            motor.setup()            
            led.setup()

        # Front LED Functions
        def  set_Front_LED_On(self,colorLED):
           led.side_on(colorLED) 
             
        def  set_Front_LED_Off(self,colorLED):
           led.side_off(colorLED) 
             

        # Ultrasonic functions

        def fetchUltraDistance(self):
            # returns cm
            distance = ultra.checkdist()*100
            return distance

        # strip LED functions

        def rainbowCycle(self, wait_ms = 20, iterations = 3):
            pixelFunctions.rainbowCycle(strip, wait_ms, iterations)

        def colorWipe(self, color):
            pixelFunctions.colorWipe(strip, color)
        
        def theaterChaseRainbow(self, wait_ms = 50):
            pixelFunctions.theaterChaseRainbow(strip, wait_ms)

        def setPixelColor(self, pixel, color, brightness):
            strip.setPixelColor(pixel, color) 
            strip.setBrightness(brightness)
            strip.show()


        # Main Motor Functions
        
        
        def motorForward(self, speed, delay):
            motor.motor_left(self.MOTOR_START, self.forward,speed)
            motor.motor_right(self.MOTOR_START, self.backward,speed)
            time.sleep(delay)
            motor.motor_left(self.MOTOR_STOP, self.forward,speed)
            motor.motor_right(self.MOTOR_STOP, self.backward,speed)
            
        def motorBackward(self, speed, delay):
            motor.motor_left(self.MOTOR_START, self.backward,speed)
            motor.motor_right(self.MOTOR_START,self.forward,speed)
            time.sleep(delay)
            motor.motor_left(self.MOTOR_STOP, self.backward,speed)
            motor.motor_right(self.MOTOR_STOP, self.forward,speed)
            
            
        def stopMotor(self):
            motor.motor_left(self.MOTOR_STOP, self.backward,0)
            motor.motor_right(self.MOTOR_STOP, self.forward,0)


        # servo motors

        # head moves

        def headTurnLeft(self):
            
            pwm.set_pwm(self.HEAD_TURN_SERVO, 0, calValues.look_left_max)
            time.sleep(0.05)

        def headTurnRight(self):
            pwm.set_pwm(self.HEAD_TURN_SERVO, 0, calValues.look_right_max)
            time.sleep(0.05)


        def headTurnMiddle(self):
            pwm.set_pwm(self.HEAD_TURN_SERVO, 0, calValues.look_turn_middle)
            time.sleep(0.05)

        def headTurnPercent(self, percent):

            adder = (calValues.look_left_max - calValues.look_right_max)*(percent/100.0)
            pwm.set_pwm(self.HEAD_TURN_SERVO, 0, int(calValues.look_left_max - adder))
            time.sleep(0.05)
            
            

        def headTiltDown(self):
            pwm.set_pwm(self.HEAD_TILT_SERVO, 0, calValues.look_down_max)       
            time.sleep(0.05)
    

        def headTiltUp(self):
            pwm.set_pwm(self.HEAD_TILT_SERVO, 0, calValues.look_up_max)
            time.sleep(0.05)


        def headTiltMiddle(self):
            pwm.set_pwm(self.HEAD_TILT_SERVO, 0, calValues.look_tilt_middle)
            time.sleep(0.05)

        def headTiltPercent(self,percent):
            adder = (calValues.look_down_max - calValues.look_up_max)*(percent/100.0)
            pwm.set_pwm(self.HEAD_TILT_SERVO, 0, int(calValues.look_down_max - adder))
            time.sleep(0.05)

        # Front Wheels

        def wheelsLeft(self):
            pwm.set_pwm(self.WHEELS_TURN_SERVO, 0, calValues.turn_left_max)
            time.sleep(0.05)


        def wheelsRight(self):
            pwm.set_pwm(self.WHEELS_TURN_SERVO, 0, calValues.turn_right_max)
            time.sleep(0.05)


        def wheelsMiddle(self):
            pwm.set_pwm(self.WHEELS_TURN_SERVO, 0, calValues.turn_middle)
            time.sleep(0.05)


        def wheelsPercent(self,percent):
            adder = (calValues.turn_left_max - calValues.turn_right_max)*(percent/100.0)
            pwm.set_pwm(self.WHEELS_TURN_SERVO, 0, int(calValues.turn_right_max + adder))
            time.sleep(0.05)



   
        # general functions



        def allLEDSOff(self):

           led.side_off(self.left_R)
           led.side_off(self.left_G)
           led.side_off(self.left_B)

           led.side_off(self.right_R)
           led.side_off(self.right_G)
           led.side_off(self.right_B)

           self.colorWipe(Color(0,0,0)) 


        def centerAllServos(self):

            self.wheelsMiddle()
            self.headTiltMiddle()
            self.headTurnMiddle()
        



