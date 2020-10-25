#
# This program uses OpenCV on the Raspberry Pi to detect a ball and then
# chase it with our robot car
# Shovic Python All-In-One for Dummies 
# October 2020
#

import traceback
import RPi.GPIO as GPIO
import motor
import ultra
import socket
import time
import threading
import picamera
from picamera.array import PiRGBArray

import cv2
from collections import deque
import numpy as np
import argparse
import imutils
import argparse
import zmq
import base64
import os
import subprocess

import neopixel
import RobotInterface 
import time
import random

#opencv frame analysis thread
def opencv_thread():         #OpenCV and FPV video
    global footage_socket, dis_data, distance_stay
    
    global hoz_mid_orig,vtr_mid_orig
    opencv_mode = 1
    font = cv2.FONT_HERSHEY_SIMPLEX

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.line(image,(300,240),(340,240),(128,255,128),1)
        cv2.line(image,(320,220),(320,260),(128,255,128),1)


        if True:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, colorLower, colorUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            cv2.imshow("OpenCV Mask", mask)
            
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
            #print("cnts=", cnts)
            center = None
            if len(cnts) > 0:
                RI.allLEDSOff()
                RI.set_Front_LED_On(RI.left_G)
                RI.set_Front_LED_On(RI.right_G)
                print("-------")
                print("target detected")
                cv2.putText(image,'Target Detected',(40,60), font, 0.5,(255,255,255),1,cv2.LINE_AA)
                c = max(cnts, key=cv2.contourArea)
                #print("c=", c)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                X = int(x)
                Y = int(y)
                #print("X=",X)
                #print("Y=",Y)
                #print ("radius=", radius)
                if radius > 10:
                    cv2.rectangle(image,(int(x-radius),int(y+radius)),(int(x+radius),int(y-radius)),(255,255,255),1)
                    
                    if X < 310:
                        mu1 = int((320-X)/3)
                        # scale mu1 to 50 (50 is the middle)
                        mu1 = int((mu1/320.0)*50.0)
                        hoz_mid_orig-=mu1
                        if hoz_mid_orig < look_left_max:
                            pass
                        else:
                            hoz_mid_orig = look_left_max
                        #print("mu1 = ", mu1)
                        #print("hoz_mid_orig=", hoz_mid_orig)
                        RI.headTurnPercent(hoz_mid_orig)
                    elif X >330:
                        mu1 = int((X-330)/3)
                        # scale to percent
                        mu1 = int((mu1/320.0)*50.0)
                        
                        hoz_mid_orig+=mu1
                        if hoz_mid_orig > look_right_max:
                            pass
                        else:
                            hoz_mid_orig = look_right_max
                        #print("mu1 = ", mu1)
                        #print("hoz_mid_orig=", hoz_mid_orig)
                        RI.headTurnPercent(hoz_mid_orig)
                        #print('x=%d'%X)
                    else:
                        RI.wheelsMiddle() 
                        pass
                    #print("hoz_mid",hoz_mid)
                    mu_t = hoz_mid_orig # can use the head angle to turn 

                    #print("turn to mu_t=", mu_t)
                    RI.wheelsPercent(mu_t)
                    
                    dis = dis_data
                    #print("dis=", dis)
                    if dis < (distance_stay-2) :
                        RI.allLEDSOff()
                        # red
                        RI.set_Front_LED_On(RI.left_R)
                        RI.set_Front_LED_On(RI.right_R)
                        
                        
                        #print("motor backward")
                        RI.motorBackward(motor_speed,motor_duration)
                        cv2.putText(image,'Too Close',(40,80), font, 0.5,(128,128,255),1,cv2.LINE_AA)
                    elif dis > (distance_stay+2):
                        #print("motor forward")
                        RI.motorForward(motor_speed,turn_motor_duration)
                        #motor.motor_left(status, forward,left_spd*spd_ad_2)
                        #motor.motor_right(status,backward,right_spd*spd_ad_2)
                        cv2.putText(image,'OpenCV Tracking',(40,80), font, 0.5,(128,255,128),1,cv2.LINE_AA)
                    else:
                        #motor.motorStop()
                        RI.stopMotor()
                        RI.allLEDSOff()
                        # blue 
                        RI.set_Front_LED_On(RI.left_B)
                        RI.set_Front_LED_On(RI.right_B)
                        cv2.putText(image,'In Position: %4.1fcm'%round(dis,1),(40,80), font, 0.5,(255,128,128),1,cv2.LINE_AA)

                    if dis < 8:
                        cv2.putText(image,'%scm'%str(round(dis,1)),(40,40), font, 0.5,(255,255,255),1,cv2.LINE_AA)

                    if Y < 230:
                        
                        mu2 = int((240-Y)/5)
                        # scale to percent
                        mu2 = int((mu2/240.0)*50.0)
                        vtr_mid_orig += mu2
                        if vtr_mid_orig < look_up_max:
                            pass
                        else:
                            vtr_mid_orig=look_up_max
                        RI.headTiltPercent(vtr_mid_orig)
                    elif Y > 250:
                        mu2 = int((Y-240)/5)
                        # scale to percent
                        mu2 = int((mu2/240.0)*50.0)
                        vtr_mid_orig -= mu2
                        if vtr_mid_orig > look_down_max:
                            pass
                        else:
                            vtr_mid_orig=look_down_max
                        RI.headTiltPercent(vtr_mid_orig)
                        
                    
                    if X>280:
                        if X<350:
                            #print('looked')
                            cv2.line(image,(300,240),(340,240),(64,64,255),1)
                            cv2.line(image,(320,220),(320,260),(64,64,255),1)
                            cv2.rectangle(image,(int(x-radius),int(y+radius)),
                                (int(x+radius),int(y-radius)),(64,64,255),1)
            else:
                RI.allLEDSOff()
                #set yellow
                #RI.set_Front_LED_On(RI.left_R)
                #RI.set_Front_LED_On(RI.left_G)
                #RI.set_Front_LED_On(RI.right_R)
                #RI.set_Front_LED_On(RI.right_G)

                cv2.putText(image,'Target Detecting',(40,60), font, 0.5,(255,255,255),1,cv2.LINE_AA)
                # this is the scan for target section of code
                #print("scaning for target")
                RI.stopMotor()
                #motor.motorStop()
                # we have nothing so start scanning
                RI.headTurnPercent(random.randint(0,100))
                RI.headTiltPercent(50)
                RI.wheelsPercent(100)
                # move back periodically to look around
                if (random.randint(0,3) == 1):
                        RI.motorBackward(motor_speed,scan_motor_duration)

                

            #print("len(pts)=", len(pts))
            for i in range(1, len(pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(image, pts[i - 1], pts[i], (0, 0, 255), thickness)
            
        else:
            dis = dis_data
            if dis < 8:
                cv2.putText(image,'%s m'%str(round(dis,2)),(40,40), font, 0.5,(255,255,255),1,cv2.LINE_AA)


        encoded, buffer = cv2.imencode('.jpg', image)
        jpg_as_text = base64.b64encode(buffer)
        footage_socket.send(jpg_as_text)
        rawCapture.truncate(0)


#display thread on Pi Screen

def video_thread():
    
    context = zmq.Context()
    my_footage_socket = context.socket(zmq.SUB)
    my_footage_socket.bind('tcp://127.0.0.1:5555')
    my_footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
    while True:
        newframe = my_footage_socket.recv_string()
        img = base64.b64decode(newframe)
        npimg = np.frombuffer(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        cv2.imshow("Stream", source)
        cv2.waitKey(1)


def dis_scan_thread():       #Get Ultrasonic scan distance
    global dis_data, dis_scan
    while 1:
        while  dis_scan:
            dis_data = RI.fetchUltraDistance() 
            #print("dis_data=", dis_data)
            time.sleep(0.2)
        time.sleep(0.2)

# main program

def mainProgram():
        global footage_socket, dis_scan
        #FPV initialization
        context = zmq.Context()
        footage_socket = context.socket(zmq.PUB)
        footage_socket.connect('tcp://127.0.0.1:5555')
        dis_scan = 1 # scan using ultrasonic

        #Threads start
        print("Starting Distance Measuring Thread")
        scan_threading=threading.Thread(target=dis_scan_thread)     #Define a thread for ultrasonic scan
        scan_threading.start()

        print("Starting Show Video Thread")
        video_show_thread=threading.Thread(target=video_thread)      #Define a thread for FPV and OpenCV
        video_show_thread.start()     

        
        print("Starting OpenCV Frame Analysis Thread")
        video_threading=threading.Thread(target=opencv_thread)      #Define a thread for FPV and OpenCV
        video_threading.start()     
        
##################################
# configuration variables
##################################


distance_stay  = 20 #stay away from target in cm
distance_range = 2 # accept this error in distance_stay (in cm)
dis_data = 0 # current ultrasonic range in cm

# head turn (hoz) and tilt middles (vtr) - In percent
vtr_mid    = 50
hoz_mid    = 50

# where they start (head turn and tilt)

hoz_mid_orig= 50
vtr_mid_orig = 50


# sets the max and minimum numbers (in percent) for head tilt and head turn
look_up_max    = 100
look_down_max  = 0 
look_right_max = 0
look_left_max  = 100

#motor speed variables - these may have to be tweaked depending on what kind of floor 
# on wich you are operating your robot.

motor_speed = 100
motor_duration = 0.40 # normal approach target duration
turn_motor_duration = 0.50 # during turn duration (needs to be a little longer)
scan_motor_duration = 0.50 # how long to back up during scan for target operations


if __name__ == '__main__':


    RI = RobotInterface.RobotInterface()
    RI.set_Front_LED_On(RI.right_G)

    camera = picamera.PiCamera()              #Camera initialization
    camera.resolution = (640, 480)
    camera.framerate = 7
    rawCapture = PiRGBArray(camera, size=(640, 480))
    
    colorLower = (65, 66, 97)                  #The HSVcolor that openCV will look for
    #colorUpper = (131, 255, 255)               #bounds for the openCV search
    colorUpper = (131, 150, 150)               #bounds for the openCV search

    ap = argparse.ArgumentParser()            #OpenCV initialization
    ap.add_argument("-b", "--buffer", type=int, default=64,
        help="max buffer size")
    args = vars(ap.parse_args())
    pts = deque(maxlen=args["buffer"])
    time.sleep(0.1)

    try:
        print("Starting Find And Chase Ball Thread")
        print("Zeroing Robot")
        RI.stopMotor()
        RI.allLEDSOff()
        RI.wheelsMiddle()
        RI.headTiltMiddle()
        RI.headTurnMiddle()
        time.sleep(0.1)
        time.sleep(5.1)
        mainProgram()
    except KeyboardInterrupt:
        RI.stopMotor()
        RI.allLEDSOff()
        RI.wheelsMiddle()
        RI.headTiltMiddle()
        RI.headTurnMiddle()
        camera=picamera.PiCamera()
        camera.close()
        destroy()

