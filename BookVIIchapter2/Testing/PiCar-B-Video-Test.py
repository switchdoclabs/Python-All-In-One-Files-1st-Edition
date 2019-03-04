#!/usr/bin/python3

DEBUG = True
VIDEOTEST = True

# runs through a video tests for the PiCar-B

import RPi.GPIO as GPIO
import motor
import ultra
import socket
import time
import threading
import turn
import led
import os
import picamera
from picamera.array import PiRGBArray
import cv2


import calValues


if __name__ == '__main__':

    camera = picamera.PiCamera()              #Camera initialization
    camera.resolution = (640, 480)
    camera.framerate = 7
    rawCapture = PiRGBArray(camera, size=(640, 480))


    try:

        print ("-------------------")
        print ("-------------------")
        print (" PiCar2- Video Test")
        print (" Must be run from a GUI")
        print ("-------------------")
        print ("-------------------")
        print ()
        print ()

        if (VIDEOTEST):

            print ()
            print ("-------------------")
            print ("Open Video Window")
            print ("-------------------")
           


            camera.resolution = (1024, 768)
            camera.start_preview(fullscreen=False, 
                    window=(100,100,256,192))
            time.sleep(20)
            camera.preview.window=(200,200,256,192)
            time.sleep(2)
            camera.preview.window=(0,0,512,384)
            time.sleep(2)
            camera.close()
    except KeyboardInterrupt:
        destroy()
