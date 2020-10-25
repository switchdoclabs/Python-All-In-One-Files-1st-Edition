#!/usr/bin/python3

DEBUG = True
LEDTEST = True
SERVOTEST = True
MOTORTEST  = True
ULTRASONICTEST = True

# runs through a set of tests for the PiCar-B

import RPi.GPIO as GPIO
import motor
import ultra
import socket
import time
import threading
import led
import os


import sys
sys.path.append("./Adafruit_PCA9685")

import Adafruit_PCA9685

import calValues

pwm = Adafruit_PCA9685.PCA9685()    
#servo mapping
# pmw 0 head tilt
HEAD_TILT_SERVO = 0
# pwm 1 head turn
HEAD_TURN_SERVO = 1
# pwm 2 wheels turn
WHEELS_TURN_SERVO = 2

#
dis_dir = []
distance_stay  = 0.4
distance_range = 2
led_status = 0

left_R = 15
left_G = 16
left_B = 18

right_R = 19
right_G = 21
right_B = 22

spd_ad     = 1          #Speed Adjustment
pwm0       = 0          #Camera direction 
pwm1       = 1          #Ultrasonic direction
status     = 1          #Motor rotation
forward    = 1          #Motor forward
backward   = 0          #Motor backward

left_spd   = 100         #Speed of the car
right_spd  = 100         #Speed of the car
left       = 100         #Motor Left
right      = 100         #Motor Right

spd_ad_1 = 1
spd_ad_2 = 1
spd_ad_u = 1

#Status of the car
auto_status   = 0
ap_status     = 0
turn_status   = 0

opencv_mode   = 0
findline_mode = 0
speech_mode   = 0
auto_mode     = 0

data = ''

dis_data = 0
dis_scan = 1







def destroy():               #Clean up
    GPIO.cleanup()



def setup_robot():                 #initialization
    motor.setup()            
    led.setup()


if __name__ == '__main__':


    # LED strip configuration:
    LED_COUNT      = 12      # Number of LED pixels.
    LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
    #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    from rpi_ws281x import *  
    import neopixel 

    from pixelFunctions import *

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()


    setup_robot()


    try:

        print ("-------------------")
        print ("-------------------")
        print (" PiCar2-Test")
        print ("-------------------")
        print ("-------------------")
        print ()
        print ()

        if (SERVOTEST):
            print ("-------------------")
            print ("-------------------")
            print ("Servo Tests")
            print ("-------------------")
            print ("-------------------")
            print ()

            print ("-------------------")
            print ("Servo Test - Head Left")
            print ("-------------------")
            pwm.set_pwm(HEAD_TURN_SERVO, 0, calValues.look_left_max)
            time.sleep(1.0)

            print ()
            print ("-------------------")
            print ("Servo Test - Head Center")
            print ("-------------------")
            pwm.set_pwm(HEAD_TURN_SERVO, 0, calValues.look_turn_middle)
            time.sleep(1.0)

            print ()
            print ()
            print ("-------------------")
            print ("Servo Test - Head Right")
            print ("-------------------")
            pwm.set_pwm(HEAD_TURN_SERVO, 0, calValues.look_right_max)
            time.sleep(1.0)
    
            print ("-------------------")
            print ("Servo Test - Head Up")
            print ("-------------------")
            pwm.set_pwm(HEAD_TILT_SERVO, 0, calValues.look_up_max)
            time.sleep(1.0)

            
            print ()
            print ("-------------------")
            print ("Servo Test - Head Down")
            print ("-------------------")
            pwm.set_pwm(HEAD_TILT_SERVO, 0, calValues.look_down_max)
            time.sleep(1.0)

            print ()
            print ("-------------------")
            print ("Servo Test - Head Tilt Straight")
            print ("-------------------")
            pwm.set_pwm(HEAD_TILT_SERVO, 0, calValues.look_tilt_middle)
            time.sleep(1.0)
            
            print ()
            print ("-------------------")
            print ("Servo Test - Wheels Left")
            print ("-------------------")

            pwm.set_pwm(WHEELS_TURN_SERVO, 0, calValues.turn_left_max)
            time.sleep(1.0)
            print ()
            print ("-------------------")
            print ("Servo Test - Wheels Center")
            print ("-------------------")

            pwm.set_pwm(WHEELS_TURN_SERVO, 0, calValues.turn_middle)
            time.sleep(1.0)
            print ()
            print ("-------------------")
            print ("Servo Test - Wheels Right")
            print ("-------------------")

            pwm.set_pwm(WHEELS_TURN_SERVO, 0, calValues.turn_right_max)
            time.sleep(1.0)
           

            
            print ("-------------------")
            print ("-------------------")
            print ("Servo Test - Straighten All ")
            print ("-------------------")
            print ("-------------------")

            print ()
            print ("-------------------")
            print ("Servo Test - Wheels Center")
            print ("-------------------")

            pwm.set_pwm(WHEELS_TURN_SERVO, 0, calValues.turn_middle)
            time.sleep(1.0)
            
            print ()
            print ("-------------------")
            print ("Servo Test - Head Center")
            print ("-------------------")
            pwm.set_pwm(HEAD_TURN_SERVO, 0, calValues.look_turn_middle)
            time.sleep(1.0)

            print ()
            print ("-------------------")
            print ("Servo Test - Head Straight")
            print ("-------------------")
            pwm.set_pwm(HEAD_TILT_SERVO, 0, calValues.look_tilt_middle)
            time.sleep(1.0)

            print()




        if (MOTORTEST): 
            print ("-------------------")
            print ("-------------------")
            print ("Motor Tests")
            print ("-------------------")
            print ("-------------------")
            print ()
            
            MOTOR_START = 1
            MOTOR_STOP = 0
       

            print ()
            print ("-------------------")
            print ("Motor Test - Forward ")
            print ("-------------------")

            motor.motor_left(MOTOR_START, forward,left_spd*spd_ad)
            motor.motor_right(MOTOR_START,backward,right_spd*spd_ad)
            time.sleep(1.0)
            motor.motor_left(MOTOR_STOP, forward,left_spd*spd_ad)
            motor.motor_right(MOTOR_STOP,backward,right_spd*spd_ad)
            

            print ()
            print ("-------------------")
            print ("Motor Test - Backward ")
            print ("-------------------")
            motor.motor_left(MOTOR_START, backward, left_spd*spd_ad)
            motor.motor_right(MOTOR_START, forward, right_spd*spd_ad)
            time.sleep(1.0)
            motor.motor_left(MOTOR_STOP, backward, left_spd*spd_ad)
            motor.motor_right(MOTOR_STOP, forward, right_spd*spd_ad)


        
        
        if (LEDTEST):
    
            print ()
            print ("-------------------")
            print ("-------------------")
            print ("LED Tests")
            print ("-------------------")
            print ("-------------------")
            print ()
    
    
            led.both_off()
            print ()
            print ("-------------------")
            print ("Left Front LED Test - Red ")
            print ("-------------------")
    
            led.side_on(led.left_R)
            time.sleep(1.0)
            led.side_off(led.left_R)
            print ()
            print ("-------------------")
            print ("Left Front LED Test - Blue ")
            print ("-------------------")
            led.side_on(led.left_B)
            time.sleep(1.0)
            led.side_off(led.left_B)
    
    
            print ()
            print ("-------------------")
            print ("Right Front LED Test - Red ")
            print ("-------------------")
            led.side_on(led.right_R)
            time.sleep(1.0)
            led.side_off(led.right_R)
    



            print ()
            print ("-------------------")
            print ("Right Front LED Test - Blue ")
            print ("-------------------")
            led.side_on(led.right_B)
            time.sleep(1.0)
            led.side_off(led.right_B)


            print ()
            print ("-------------------")
            print ("Both Police LED Test - On ")
            print ("-------------------")
   
            led.police(2)

            print ()
            print ("-------------------")
            print ("12 RGB Pixel LED Test - On ")
            print ("-------------------")
        
            rainbowCycle(strip, wait_ms=20, iterations=3)
    
            print ()
            print ("-------------------")
            print ("12 RGB Pixel LED Test - Off ")
            print ("-------------------")
    
            colorWipe(strip, Color(0,0,0)) 

        if (ULTRASONICTEST):
    
            print ()
            print ("-------------------")
            print ("Ultrasonic Distance Test")
            print ("-------------------")

            average_distance = 0.0
            for i in range(0,10):
                distance = ultra.checkdist()
                average_distance = average_distance + distance
                print ("Distance = {:6.3f}cm ".format( distance*100))
                time.sleep(1.0)
            average_distance = average_distance / 10 

            print ("average_distance = {:6.3f}cm".format(average_distance*100))
                    
    except KeyboardInterrupt:
        destroy()
