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
Move(1, 900, 150)
Move(2, 550, 150)
Move(3, -300, 150)
Move(4, 900, 150)
Move(5, 550, 150)
Move(6, -300, 150)
Move(7, -900, 150)
Move(8, -550, 150)
Move(9, 300, 150)
Move(10, -900, 150)
Move(11, -550, 150)
Move(12, 300, 150)
Move(13, 0, 150)
Move(14, 0, 150)
time.sleep(2)


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
def Forward(): 
               x = float(0.0)
               y = float(10.0)
               z = float(-155.0)
               for i in range(15):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 54.2,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)

                 Move(1, (sheta3-450), 0.1)
                 Move(2,(sheta2), 0.1)
                 Move(3, -sheta1+330, 0.1)
                 Move(4, 59-(sheta3-450), 0.1)
                 Move(5, -801-sheta2, 0.1)
                 Move(6, sheta1+330, 0.1) 
                
                 Move(7, -400, 20)
                 Move(8, 100, 30)
                 Move(9, -sheta1-330, 30)
                 Move(10, -600, 30)
                 Move(11, 150, 10)
                 Move(12, sheta1-330, 30)
                 Move(17, 200, 10)
                 Move(16, 1000, 10)
                 Move(15, -1000, 10)
                 y+= 0.6   
               x = float(0.0)
               y = float(10.0)
               z = float(-155.0)
               for i in range(15):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
         
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 54.2,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)         
                 Move(10, 59+(-sheta3+450), 0.1)
                 Move(11, 801-(-sheta2), 0.1)
                 Move(12, -sheta1-330, 0.1)
                 Move(7, (-sheta3+450), 0.1)
                 Move(8, -sheta2, 0.1)
                 Move(9, sheta1-330, 0.1)
                
                 Move(1, 400, 20)
                 Move(2, -100, 30)
                 Move(3, sheta1+330, 30)
                 Move(4, 600, 30)
                 Move(5, -150, 10)
                 Move(6, -sheta1+330, 30)
                 y += 0.6
                 print sheta3
                 print sheta2
             
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def Right():          
               x = float(1.5)
               y = float(5.0)
               z = float(-150.0)
               for i in range(20):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 54.2,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 Move(1, sheta3-450, 3)
                 Move(2, sheta2, 3)
                 Move(3, sheta1-300, 3)
                 Move(4, sheta3-450, 3)
                 Move(5, sheta2, 3)
                 Move(6, sheta1-300, 3) 
                
                 Move(7, -250, 3)
                 Move(8, 250, 3)
                 Move(9, -sheta1+300, 3)
                 Move(10, -250, 3)
                 Move(11, 250, 3)
                 Move(12, -sheta1+300, 3)
                 x-= 0.15  
               x = float(1.5)
               y = float(5.0)
               z = float(-150.0)
               for i in range(20):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 118.0,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 
                 Move(10, -sheta3+450, 3)
                 Move(11, -sheta2, 3)
                 Move(12, sheta1+300, 3)
                 Move(7, -sheta3+450, 3)
                 Move(8, -sheta2, 3)
                 Move(9, sheta1+300, 3) 
                
                 Move(1, 250, 3)
                 Move(2, -250, 3)
                 Move(3, -sheta1-300, 3)
                 Move(4, 250, 3)
                 Move(5, -250, 3)
                 Move(6, -sheta1-300, 3)
                 x-= 0.15
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def Left():          
               x = float(1.5)
               y = float(5.0)
               z = float(-150.0)
               for i in range(20):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 54.2,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 Move(7, -sheta3+450, 3)
                 Move(8, -sheta2, 3)
                 Move(9, -sheta1+300,3)
                 Move(10, -sheta3+450, 3)
                 Move(11, -sheta2, 3)
                 Move(12, -sheta1+300, 3) 
                
                 Move(1, 250, 3)
                 Move(2, -250, 3)
                 Move(3, sheta1-300, 3)
                 Move(4, 250, 3)
                 Move(5, -250, 3)
                 Move(6, sheta1-300, 3)
                 x-= 0.15 
               x = float(1.5)
               y = float(5.0)
               z = float(-150.0)
               for i in range(20):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 54.2,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 Move(4, sheta3-450, 3)
                 Move(5, sheta2, 3)
                 Move(6, -sheta1-300,3)
                 Move(1, sheta3-450, 3)
                 Move(2, sheta2, 3)
                 Move(3, -sheta1-300, 3) 
                  
                 Move(7,  -250, 3) 
                 Move(8, 250, 3) 
                 Move(9,  sheta1+300, 3)
                 Move(10, -250, 3)
                 Move(11, 250, 3)
                 Move(12, sheta1+300, 3)
                 x-=0.15
#////////////////////////////////////////////////////////////////////////////                  
def Back():

               x = float(0.0)
               y = float(10.0)
               z = float(-155.0)
               for i in range(15):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 54.2,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)

                 Move(1, 59-(sheta3-450), 0.1)
                 Move(2,-801-(sheta2), 0.1)
                 Move(3, -sheta1+330, 0.1)
                 Move(4, (sheta3-450), 0.1)
                 Move(5, sheta2, 0.1)
                 Move(6, sheta1+330, 0.1) 
                
                 Move(7, -600, 30)
                 Move(8, 150, 10)
                 Move(9, -sheta1-330, 30)
                 Move(10, -400, 20)
                 Move(11, 100, 30)
                 Move(12, sheta1-330, 30)
                 Move(17, 200, 10)
                 Move(16, 300, 10)
                 Move(15, 300, 10)
                 y+= 0.6   
               x = float(0.0)
               y = float(10.0)
               z = float(-155.0)
               for i in range(15):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
         
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 54.2,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)         
                 Move(10, (-sheta3+450), 0.1)
                 Move(11, (-sheta2), 0.1)
                 Move(12, -sheta1-330, 0.1)
                 Move(7, 59+(-sheta3+450), 0.1)
                 Move(8, 801-(-sheta2), 0.1)
                 Move(9, sheta1-330, 0.1)
                
                 Move(1, 600, 30)
                 Move(2, -150, 10)
                 Move(3, sheta1+330, 30)
                 Move(4, 400, 20)
                 Move(5, -100, 30)
                 Move(6, -sheta1+330, 30)
                 y += 0.6
                 print sheta3
                 print sheta2
def Right_forward():          
               x = float(1.0)
               y = float(10.0)
               z = float(-155.0)
               for i in range(20):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 54.2,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 Move(1, sheta3-450, 1)
                 Move(2, sheta2, 1)
                 Move(3, sheta1+450, 1)
                 Move(4, sheta3-450, 1)
                 Move(5, sheta2, 1)
                 Move(6, -sheta1+450, 1) 
                
                 Move(7, -250, 4)
                 Move(8, 200, 4)
                 Move(9, 150-450, 4)
                 Move(10, -250, 4)
                 Move(11, 200, 4)
                 Move(12, 0-450, 4)
                 x-= 0.1  
               x = float(1.0)
               y = float(10.0)
               z = float(-155.0)
               for i in range(20):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 118.0,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 
                 Move(10, -sheta3+450, 1)
                 Move(11, -sheta2, 1)
                 Move(12, -sheta1-450, 1)
                 Move(7, -sheta3+450, 1)
                 Move(8, -sheta2, 1)
                 Move(9, sheta1-450, 1) 
                
                 Move(1, 250, 4)
                 Move(2, -200, 4)
                 Move(3, -0+450, 4)
                 Move(4, 250, 4)
                 Move(5, -200, 4)
                 Move(6, -150+450, 4)
                 x-= 0.1
#/////////////////////////////////////////////////////////////////////////
def Left_forward():          
               x = float(-1.0)
               y = float(10.0)
               z = float(-155.0)
               for i in range(20):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 54.2,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 Move(1, sheta3-450, 1)
                 Move(2, sheta2, 1)
                 Move(3, sheta1+450, 1)
                 Move(4, sheta3-450, 1)
                 Move(5, sheta2, 1)
                 Move(6, -sheta1+450, 1) 
                
                 Move(7, -250, 4)
                 Move(8, 200, 4)
                 Move(9, 0-450, 4)
                 Move(10, -250, 4)
                 Move(11, 200, 4)
                 Move(12, 150-450, 4)
                 x+= 0.1  
               x = float(-1.0)
               y = float(10.0)
               z = float(-155.0)
               for i in range(20):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 118.0,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 
                 Move(10, -sheta3+450, 1)
                 Move(11, -sheta2, 1)
                 Move(12, -sheta1-450, 1)
                 Move(7, -sheta3+450, 1)
                 Move(8, -sheta2, 1)
                 Move(9, sheta1-450, 1) 
                
                 Move(1, 250, 4)
                 Move(2, -200, 4)
                 Move(3, -150+450, 4)
                 Move(4, 250, 4)
                 Move(5, -200, 4)
                 Move(6, -00+450, 4)
                 x+= 0.1
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def stop():  
             Move(1, -100, 200)
             Move(2, -500, 200)
             Move(3, -300, 200)
             Move(4, -100, 200)
             Move(5, -500, 200)
             Move(6, -300, 200)
             Move(7, 100, 200)
             Move(8, 500, 200)
             Move(9, 300, 200)
             Move(10, 100, 200)
             Move(11, 500, 200)
             Move(12, 300, 200)
             Move(17, 0, 200)
             Move(16, 1000, 200)
             Move(15, 1000, 200)
            
def ball_get():
             Move(13, -300, 50)
             Move(14, 300, 50)
             Move(1, 1100, 150)
             Move(2, 900, 150)
             Move(3, -100, 150)
             Move(4, 850, 150)
             Move(5, 500, 150)
             Move(6, -300, 150)
             Move(7, -1100, 150)
             Move(8, -900, 150)
             Move(9, 100, 150)
             Move(10, -850, 150)
             Move(11, -500, 150)
             Move(12, 300, 150)
             time.sleep(2)
             Move(13, 50, 50)
             Move(14, -50, 50)

def ball_shoot():
            
             Move(1, 1100, 100)
             Move(2, 700, 100)
             Move(3, -300, 100)
             Move(4, -300, 100)
             Move(5, -800, 100)
            # Move(6, -300, 100)
             Move(7, -1100, 100)
             Move(8, -700, 100)
             Move(9, 300, 100)
             Move(10, 300, 100)
             Move(11, 800, 100)
            # Move(12, 300, 100)
             time.sleep(1)
             
             Move(13, -10, 50)
             Move(14, 10, 50)
             time.sleep(1.5)
             Move(13,0, 50)
             Move(14, 0, 50)

def hill_forward():          
               x = float(1.5)
               y = float(5.0)
               z = float(-150.0)
               for i in range(30):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 54.2,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 Move(1, sheta3-450, 3)
                 Move(2, sheta2, 3)
                 Move(3, sheta1-450, 3)
                 Move(4, sheta3-450, 3)
                 Move(5, sheta2, 3)
                 Move(6, -sheta1-450, 3) 
                
                 Move(7, -250, 3)
                 Move(8, 250, 3)
                 Move(9, sheta1+450, 3)
                 Move(10, -250, 3)
                 Move(11, 250, 3)
                 Move(12, -sheta1+450, 3)
                 x-= 0.1  
               x = float(1.5)
               y = float(5.0)
               z = float(-150.0)
               for i in range(30):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 118.0,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 
                 Move(10, -sheta3+450, 3)
                 Move(11, -sheta2, 3)
                 Move(12, sheta1+450, 3)
                 Move(7, -sheta3+450, 3)
                 Move(8, -sheta2, 3)
                 Move(9, -sheta1+450, 3) 
                
                 Move(1, 250, 3)
                 Move(2, -250, 3)
                 Move(3, -sheta1-450, 3)
                 Move(4, 250, 3)
                 Move(5, -250, 3)
                 Move(6, sheta1-450, 3)
                 x-= 0.1

def hill_back():          
               x = float(1.5)
               y = float(5.0)
               z = float(-150.0)
               for i in range(30):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 54.2,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 Move(1, sheta3-450, 0.1)
                 Move(2, sheta2, 0.1)
                 Move(3, -sheta1-450, 0.1)
                 Move(4, sheta3-450, 0.1)
                 Move(5, sheta2, 0.1)
                 Move(6, sheta1-450, 0.1) 
                
                 Move(7, -250, 0.1)
                 Move(8, 200, 0.1)
                 Move(9, -sheta1+450, 0.1)
                 Move(10, -250, 0.1)
                 Move(11, 200, 0.1)
                 Move(12, sheta1+450, 0.1)
                 x-= 0.1  
               x = float(1.5)
               y = float(5.0)
               z = float(-150.0)
               for i in range(30):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 118.0,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 
                 Move(10, -sheta3+450, 0.1)
                 Move(11, -sheta2, 0.1)
                 Move(12, -sheta1+450, 0.1)
                 Move(7, -sheta3+450, 0.1)
                 Move(8, -sheta2, 0.1)
                 Move(9, sheta1+450, 0.1) 
                
                 Move(1, 250, 0.1)
                 Move(2, -200, 0.1)
                 Move(3, sheta1-450, 0.1)
                 Move(4, 250, 0.1)
                 Move(5, -200, 0.1)
                 Move(6, -sheta1-450, 0.1)
                 x-= 0.1

def Hill_Forward():          
               x = float(3.0)
               y = float(5.0)
               z = float(-150.0)
               for i in range(40):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 54.2,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 Move(1, sheta3-450, 3)
                 Move(2, sheta2, 3)
                 Move(3, sheta1-450, 3)
                 Move(4, sheta3-450, 3)
                 Move(5, sheta2, 3)
                 Move(6, -sheta1-450, 3) 
                
                 Move(7, -500, 3)
                 Move(8, -100, 3)
                 Move(9, sheta1+250, 3)
                 Move(10, -250, 3)
                 Move(11, 300, 3)
                 Move(12, -sheta1+550, 3)
                 Move(17, 700,1)
                 Move(16, -800,1)
                 Move(15, -450, 1)
                 x-= 0.1
               Move(16, -300, 0.3)
               Move(17,-300, 0.3)
               Move(15, -200, 0.3)
               time.sleep(0.3)
                   
               x = float(3.0)
               y = float(5.0)
               z = float(-150.0)
               for i in range(40):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 118.0,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 
                 Move(10, -sheta3+450, 3)
                 Move(11, -sheta2, 3)
                 Move(12, sheta1+450, 3)
                 Move(7, -sheta3+450, 3)
                 Move(8, -sheta2, 3)
                 Move(9, -sheta1+450, 3) 
                
                 Move(1, 500, 3)
                 Move(2, 100, 3)
                 Move(3, -sheta1-250, 3)
                 Move(4, 250, 3)
                 Move(5, -300, 3)
                 Move(6, sheta1-550, 3)
                 Move(17, -700,1)
                 Move(16, -800,1)
                 Move(15, -450, 1)
                 x-= 0.1
               Move(16, -300,0.3)
               Move(17,300, 0.3)
               Move(15, -200, 0.3)
               time.sleep(0.3)    

def Hill_Back():          
               x = float(2.0)
               y = float(5.0)
               z = float(-150.0)
               for i in range(40):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 54.2,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 Move(1, sheta3-450, 3)
                 Move(2, sheta2, 3)
                 Move(3, -sheta1-450, 3)
                 Move(4, sheta3-450, 3)
                 Move(5, sheta2, 3)
                 Move(6, sheta1-450, 3) 
                
                 Move(7, -250, 3)
                 Move(8, 300, 3)
                 Move(9, -sheta1+450, 3)
                 Move(10, -250, 3)
                 Move(11, 200, 3)
                 Move(12, sheta1+450, 3)
                 Move(17, 700,1)
                 Move(16, -700,1)
                 Move(15, -450, 1)
                 x-= 0.1
               Move(16, -300, 0.3)
               Move(17,-300, 0.3)
               Move(15, -200, 0.3)
               time.sleep(0.3)
                   
               x = float(2.0)
               y = float(5.0)
               z = float(-150.0)
               for i in range(40):
                 sheta1rad = float(math.atan2(x, y))
                 sheta1 = float((sheta1rad* 180.0 / PI)*10)
                 print sheta1
            
                 C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
                 
                 sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
                 sheta3 = float((sheta3rad*180.0 / PI)*10)
                 k = float(math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2))
                 g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 118.0,2))
                 a = float(math.cos(sheta3rad)*118.0+54.2)
                 
                 sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
                 sheta2 = float((sheta2rad*180.0 / PI)*10)
                 
                 Move(10, -sheta3+450, 3)
                 Move(11, -sheta2, 3)
                 Move(12, -sheta1+450, 3)
                 Move(7, -sheta3+450, 3)
                 Move(8, -sheta2, 3)
                 Move(9, sheta1+450, 3) 
                
                 Move(1, 250, 3)
                 Move(2, -300, 3)
                 Move(3, sheta1-450, 3)
                 Move(4, 250, 3)
                 Move(5, -200, 3)
                 Move(6, -sheta1-450, 3)
                 Move(17, -700,1)
                 Move(16, -700,1)
                 Move(15, -450, 1)
                 x-= 0.1
               Move(16, -300,0.3)
               Move(17,300, 0.3)
               Move(15, -200, 0.3)
               time.sleep(0.3)    

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                       
if __name__ == '__main__':                   
     M = Mode_C()






     while 1:
        print 9
        rospy.init_node('A')
        A = JoyTwist()
        if mode == 1:
            #M.hill_forward()
            M.Forward()
            print "Forward"
        elif mode == 2:
            Right()
            print "Right"
        elif mode == 3:
            Left()
            print "Left"
        elif mode == 4:
            hill_back()
            print "Back"
        elif mode == 5:
            ball_get()
            print "ball_get"
            time.sleep(3)
        elif mode == 6:
            ball_shoot()
            print "ball_shoot"
            time.sleep(3)
        elif mode == 7:
            #Right_forward()
            print "Right_forward"
        elif mode == 8:
            #Left_forward()
            print "Left_forward"
        elif mode == 9:
            Hill_Forward()
            print "hill_forward"
        elif mode == 10:
            Hill_Back()
            print "hill_back"
        else:
            stop()
            print "stop"
            
       # rospy.spin()
servo.close()
