#!/usr/bin/env python
#-*- coding:utf-8 -*-

# torque checkbit error

import rospy
import serial
import time
import sys
import math
from sensor_msgs.msg import Joy
from ros_start.Mode import Mode_C
from geometry_msgs.msg import Twist
PI = math.pi
servo = serial.Serial('/dev/ttyS0',115200)
TORQUE_ON = 0xFF
time.sleep(0.5)
fg=0
mode = 0

# torque ON
def Torque(ID, sw):
        check = 0x00
        TxData = [0xFA, 0xAF, ID, 0x00, 0x24, 0x01,0x01,sw]
        for i in range(2,8):
                check = check^TxData[i]
        TxData.append(check)
        servo.write(TxData)
        time.sleep(0.00025)
               
Torque(0xFF,0x01)
time.sleep(1)


class JoyTwist(object):
    
    def __init__(self):
        self._joy_sub = rospy.Subscriber('joy', Joy,self.joy_callback, queue_size=1)
        self._twist_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)
    def joy_callback(self,joy_msg):    
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 
           global mode
           mode = 0
           twist = Twist()
           if joy_msg.axes[1] >0.9:
              fg = 1
              mode = 1
              print "forward joy_callback" 
           elif joy_msg.axes[3] <-0.9:
              fg = 1
              mode =2
              print "right joy_callback" 
           elif joy_msg.axes[3] > 0.9:
              fg = 1
              mode = 3
              print "left joy_callback"    
           elif joy_msg.axes[1] <-0.9:
              fg = 1
              mode =4
              print "back joy_callback"
           elif joy_msg.buttons[1] == 1:
              mode =5
              print "ball get joy_callback" 
           elif joy_msg.buttons[0] ==1:
              mode =6
              print "ball shoot joy_callback"
           elif joy_msg.axes[0] <-0.9:
              mode =7
              print "right forward joy_callback"
           elif joy_msg.axes[0] >0.9:
              mode =8
              print "left forward joy_callback"
           elif joy_msg.axes[4] >0.9:
              mode =9
              print "hill forward joy_callback"
           elif joy_msg.axes[4] <-0.9:
              mode =10
              print "hill back joy_callback"
           else:
              fg = 0
              print "4 joy_callback" 
                 

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                       
if __name__ == '__main__':                   
     M = Mode_C()
     M.Stand_up()
     time.sleep(2)
     while 1:
        rospy.init_node('A')
        A = JoyTwist()
        if mode == 1:
            M.Forward()
            print "Forward"
        elif mode == 2:
            M.CW()
            print "CW"
        elif mode == 3:
            M.CCW()
            print "CCW"
        elif mode == 4:
            M.Back()
            print "Back"
        elif mode == 5:
            M.ball_get()
            print "ball_get"
            time.sleep(3)
        elif mode == 6:
            M.ball_shoot()
            print "ball_shoot"
            time.sleep(3)
        elif mode == 7:
            #Right_forward()
            print "Right_forward"
        elif mode == 8:
            #Left_forward()
            print "Left_forward"
        elif mode == 9:
            M.Hill_Forward()
            print "hill_forward"
        elif mode == 10:
            M.Hill_Back()
            print "hill_back"
        else:
            M.Stop()
            print "stop"
            
       # rospy.spin()
servo.close()
