#!/usr/bin/env python
#-*- coding:utf-8 -*-

# torque checkbit error

import rospy
import serial
import time
import sys
import math
from sensor_msgs.msg import Joy
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


#move
def Move(ID, Angle, Speed):
        check = 0x00
        Angle = int(Angle)
        Speed = int(Speed)
        TxData = [\
                   0xFA,0xAF,ID,0x00,0x1E,0x04,0x01,\
                   0x00FF&Angle,0x00FF&(Angle >> 8),\
                   0x00FF&Speed, 0x00FF&(Speed >> 8)\
                 ]
        for i in range(2,11):
                   check = check^TxData[i]
        TxData.append(check)
        servo.write(TxData)
        time.sleep(0.00025)
               
Torque(0xFF,0x01)
time.sleep(1)
print 0
Move(1, 900, 30)
Move(2, 0, 30)
Move(3, 0, 30)
Move(4, 900, 30)
Move(5, 0, 30)
Move(6, 0, 30)
Move(7, -900, 30)
Move(8, 0, 30)
Move(9, 0, 30)
Move(10, -900, 30)
Move(11, 0, 30)
Move(12, 0, 30)
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
              print "1 joy_callback" 
           elif joy_msg.axes[3] <-0.9:
              fg = 1
              mode =2
              print "2 joy_callback" 
           elif joy_msg.axes[3] > 0.9:
              fg = 1
              mode = 3
              print "3 joy_callback" 
           else:
              fg = 0
              print "4 joy_callback" 
def mode1(): 
               x = float(35.0)
               y = float(125.0)
               z = float(80.0)
               for i in range(14):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(63.4,2)) /(2*54.2*63.4)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(63.4,2))-pow(math.cos(sheta3rad)*63.4 + 54.2,2))
                 a = float(math.cos(sheta3rad)*63.4+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*63.4)-a*z)/g,(-k*a-(math.sin(sheta3rad)*63.4*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 Move(1, sheta3, 0.5)
                 Move(2, sheta2, 0.5)
                 Move(3, -sheta1, 0.5)
                 Move(4, sheta3, 0.5)
                 Move(5, sheta2, 0.5)
                 Move(6, sheta1, 0.5) 
                
                 Move(7, -sheta3, 0.5)
                 Move(8, 350, 0.5)
                 Move(9, -sheta1, 0.5)
                 Move(10, -sheta3, 0.5)
                 Move(11, 350, 0.5)
                 Move(12, sheta1, 0.5)
                 x-= 5    
               x = float(35.0)
               y = float(125.0)
               z = float(80.0)
               for i in range(14):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
         
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(63.4,2)) /(2*54.2*63.4)))
                
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(63.4,2))-pow(math.cos(sheta3rad)*63.4 + 54.2,2))
                 a = float(math.cos(sheta3rad)*63.4+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*63.4)-a*z)/g,(-k*a-(math.sin(sheta3rad)*63.4*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)         
                 Move(10, -sheta3, 0.5)
                 Move(11, -sheta2, 0.5)
                 Move(12, -sheta1, 0.5)
                 Move(7, -sheta3, 0.5)
                 Move(8, -sheta2, 0.5)
                 Move(9, sheta1, 0.5)
                
                 Move(1, sheta3, 1)
                 Move(2, -350, 1)
                 Move(3, sheta1, 1)
                 Move(4, sheta3, 1)
                 Move(6, -sheta1, 1)
                 x -= 5
             
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def mode2():          
               x = float(15.0)
               y = float(70.0)
               z = float(100.0)
               for i in range(10):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(63.4,2)) /(2*54.2*63.4)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(63.4,2))-pow(math.cos(sheta3rad)*63.4 + 54.2,2))
                 a = float(math.cos(sheta3rad)*63.4+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*63.4)-a*z)/g,(-k*a-(math.sin(sheta3rad)*63.4*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 Move(1, sheta3, 1)
                 Move(2, sheta2, 1)
                 Move(3, sheta1, 1)
                 Move(4, sheta3, 1)
                 Move(5, sheta2, 1)
                 Move(6, sheta1, 1) 
                
                 Move(7, -450, 1)
                 Move(8, 100, 1)
                 Move(9, 100, 1)
                 Move(10, -450, 1)
                 Move(11, 100, 1)
                 Move(12, 100, 1)
                 x-= 2  
               x = float(15.0)
               y = float(70.0)
               z = float(100.0)
               for i in range(10):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(63.4,2)) /(2*54.2*63.4)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(63.4,2))-pow(math.cos(sheta3rad)*63.4 + 54.2,2))
                 a = float(math.cos(sheta3rad)*63.4+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*63.4)-a*z)/g,(-k*a-(math.sin(sheta3rad)*63.4*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 
                 Move(10, -sheta3, 0.5)
                 Move(11, -sheta2, 0.5)
                 Move(12, sheta1, 0.5)
                 Move(7, -sheta3, 0.5)
                 Move(8, -sheta2, 0.5)
                 Move(9, sheta1, 1) 
                
                 Move(1, 450, 1)
                 Move(2, -100, 1)
                 Move(3, 100, 1)
                 Move(4, 450, 1)
                 Move(5, -100, 1)
                 Move(6, 100, 1)
                 x-= 2      
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def mode3():          
               x = float(15.0)
               y = float(70.0)
               z = float(100.0)
               for i in range(10):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(63.4,2)) /(2*54.2*63.4)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(63.4,2))-pow(math.cos(sheta3rad)*63.4 + 54.2,2))
                 a = float(math.cos(sheta3rad)*63.4+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*63.4)-a*z)/g,(-k*a-(math.sin(sheta3rad)*63.4*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 Move(7, -sheta3, 1)
                 Move(8, -sheta2, 1)
                 Move(9, -sheta1,1)
                 Move(10, -sheta3, 1)
                 Move(11, -sheta2, 1)
                 Move(12, -sheta1, 1) 
                
                 Move(1, 450, 1)
                 Move(2, -100, 1)
                 Move(3, -100, 1)
                 Move(4, 450, 1)
                 Move(5, -100, 1)
                 Move(6, -100, 1)
                 x-= 2 
               x = float(15.0)
               y = float(70.0)
               z = float(100.0)
               for i in range(10):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(63.4,2)) /(2*54.2*63.4)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(63.4,2))-pow(math.cos(sheta3rad)*63.4 + 54.2,2))
                 a = float(math.cos(sheta3rad)*63.4+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*63.4)-a*z)/g,(-k*a-(math.sin(sheta3rad)*63.4*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 Move(4, sheta3, 1)
                 Move(5, sheta2, 1)
                 Move(6, -sheta1,1)
                 Move(1, sheta3, 1)
                 Move(2, sheta2, 1)
                 Move(3, -sheta1, 1) 
                  
                 Move(7,  -450, 1) 
                 Move(8, 100, 1) 
                 Move(9,  -100, 1)
                 Move(10, -450, 1)
                 Move(11, 100, 1)
                 Move(12, -100, 1)
                 x-=2
                  
def stop():  
             Move(1, 900, 30)
             Move(2, 0, 30)
             Move(3, 0, 30)
             Move(4, 900, 30)
             Move(5, 0, 30)
             Move(6, 0, 30)
             Move(7, -900, 30)
             Move(8, 0, 30)
             Move(9, 0, 30)
             Move(10, -900, 30)
             Move(11, 0, 30)
             Move(12, 0, 30)
                   
if __name__ == '__main__':                   
     while 1:
        print 9
        rospy.init_node('A')
        A = JoyTwist()
        if mode == 1:
            mode1()
            print "11 main"
        elif mode == 2:
            mode2()
            print "22 main"
        elif mode == 3:
            mode3()
            print "33 main"
        else:
            stop()
            print "44 main"
            
       # rospy.spin()
servo.close()
