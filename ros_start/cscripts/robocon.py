#!/usr/bin/env python
#-*- coding:utf-8 -*-

# torque checkbit error

import rospy
import serial
import time
import sys
import math
from std_msgs.msg import Int32
from ros_start.Mode import Mode_C

PI = math.pi
servo = serial.Serial('/dev/ttyS0', 115200)
TORQUE_ON = 0xFF

def Torque(ID, sw):
    check = 0x00
    TxDate = [0xFA, 0xAF, ID, 0x00, 0x24, 0x01, 0x01, sw]
      
    for i in range(2, 8):
        check = check^TxDate[i]
      
    TxDate.append(check)  
    servo.write(TxDate)
    time.sleep(0.00025)

    
class Q_4L(object):
    def __init__(self):
        self.mode_sub = rospy.Subscriber('/chan_yagi', Int32, self.callback)

        

    def callback(self, data):
        print('input')
        ya = data.data
        if ya == 1:
            print("Forward")
            mode.Forward()
        if ya == 2:
            print("CW")
            mode.CW()
        if ya == 3:
            print("CCW")
            mode.CCW()
        if ya == 4:
            print("Back")
            mode.Back()
        if ya == 5:
            print("Hill_Forward")
            mode.Hill_Forward()
        if ya == 6:
            print("Hill_Back")
            mode.Hill_Back()
        if ya == 7:
            print("ball_get")
            mode.ball_get()
        if ya == 8:
            print("ball_shoot")
            mode.ball_get()
        if ya == 9:
            print("Stand_up")
            mode.Stand_up()
        if ya == 10:
            print("Stop")
            mode.Stop()


        
    

if __name__ == '__main__':
    Torque(0xFF, 0x01)
    time.sleep(1) 
    mode = Mode_C()
    mode.Stand_up()
    time.sleep(2)
    mode.Stop() #stand_up   
    time.sleep(1)

    rospy.init_node("Robocon")
    print('aaaaa')
    robocon = Q_4L()
    rospy.spin()
servo.close()
