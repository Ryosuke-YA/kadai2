#!/usr/bin/env python 
#-*- coding:utf-8 -*-

# torque checkbit error

import roslib
import rospy
import serial
import math
import time
from ros_start.kinematics import Kinematics_f

servo = serial.Serial('/dev/ttyS0', 115200)

class Mode_C(object):
    def Move(self, ID, Angle, Speed):
        check = 0x00
        Angle = int(Angle)
        Speed = int(Speed)
        TxDate = [\
                    0xFA, 0XAF, ID, 0x00, 0x1E, 0x04, 0x01,\
                    0x00FF&Angle, 0x00FF&(Angle >> 8),\
                    0x00FF&Speed, 0x00FF&(Speed >> 8)\
                 ]
        
        for i in range(2, 11):
            check = check^TxDate[i]
     
        TxDate.append(check)
        servo.write(TxDate)
        time.sleep(0.00025)


    def Stand_up(self):
        self.Move(1, 900, 150)
        self.Move(2, 450, 150)
        self.Move(3, -400, 150)
        self.Move(4, 900, 150)
        self.Move(5, 550, 150)
        self.Move(6, -400, 150)
        self.Move(7, -900, 150)
        self.Move(8, -450, 150)
        self.Move(9, 400, 150)
        self.Move(10, -900, 150)
        self.Move(11, -550, 150)
        self.Move(12, 400, 150)
        self.Move(13, 0, 150)
        self.Move(14, 0, 150)

    def Stop(self):
        self.Move(1, -50, 100)
        self.Move(2, -350, 100)
        self.Move(3, -400, 100)
        self.Move(4, -100, 100)
        self.Move(5, -500, 100)
        self.Move(6, -400, 100)
        self.Move(7, 50, 100)
        self.Move(8, 350, 100)
        self.Move(9, 400, 100)
        self.Move(10, 100, 100)
        self.Move(11, 500, 100)
        self.Move(12, 400, 100)
        self.Move(17, 0, 100)
        self.Move(16, 1000, 100)
        self.Move(15, 1000, 100)



    def Forward(self):
        x = float(10.0)
        y = float(70.0)
        z = float(-165.0)
        x2 = float(0.0)
        y2 = float(70.0)
        z2 = float(-165.0)
        for i in range(20):
            sheta1, sheta2, sheta3 = Kinematics_f(x, y, z) 
            sheta11, sheta22, sheta33 = Kinematics_f(x2, y2, z2) 
            self.Move(1, sheta3-450, 3)
            self.Move(2, sheta2, 3)
            self.Move(3, sheta1-450, 3)
            self.Move(4, sheta33-450, 3)
            self.Move(5, sheta22, 3)
            self.Move(6, -sheta11-450, 3)

            self.Move(7, -200, 3)
            self.Move(8, 250, 3)
            self.Move(9, sheta1+450, 3)
            self.Move(10, -200, 3)
            self.Move(11, 250, 3)
            self.Move(12, -sheta11+450, 3)
            self.Move(17, 0, 3)
            self.Move(16, 1000, 3)
            self.Move(15, 1000, 3)

            x -= 1.5
            x2 -= 1.5

        x = float(10.0) 
        y = float(70.0)
        z = float(-165.0)
        x2 = float(0.0)
        y2 = float(70.0)
        z2 = float(-165.0)
        for i in range(20):
            sheta1, sheta2, sheta3 = Kinematics_f(x, y, z)
            sheta11, sheta22, sheta33 = Kinematics_f(x2, y2, z2) 
            self.Move(10, (-sheta33+450), 3)
            self.Move(11, -sheta22, 3)
            self.Move(12, sheta11+450, 3)
            self.Move(7, -sheta3+450, 3)
            self.Move(8, -sheta2, 3)
            self.Move(9, -sheta1+450, 3)

            self.Move(1, 200, 3)
            self.Move(2, -250, 3)
            self.Move(3, -sheta1-450, 3)
            self.Move(4, 200, 3)
            self.Move(5, -250, 3)
            self.Move(6, sheta11-450, 3)
            self.Move(17, 0, 3)
            self.Move(16, 1000, 3)
            self.Move(15, 1000, 3)
            x -= 1.5
            x2 -= 1.5


    def CCW(self):
            x = float(3.0)
            y = float(20.0)
            z = float(-155.0)
            for i in range(20):
                 sheta1, sheta2, sheta3 = Kinematics_f(x, y, z)
                 self.Move(7, -sheta3+450, 3)
                 self.Move(8, -sheta2, 3)
                 self.Move(9, -sheta1+400,3)
                 self.Move(10, -sheta3+450, 3)
                 self.Move(11, -sheta2, 3)
                 self.Move(12, -sheta1+400, 3) 
                
                 self.Move(1, 250, 3)
                 self.Move(2, -250, 3)
                 self.Move(3, sheta1-400, 3)
                 self.Move(4, 250, 3)
                 self.Move(5, -250, 3)
                 self.Move(6, sheta1-400, 3)
                 x-= 0.3 
            x = float(3.0)
            y = float(20.0)
            z = float(-155.0)
            for i in range(20):
                 sheta1, sheta2, sheta3 = Kinematics_f(x, y, z)
                 self.Move(4, sheta3-450, 3)
                 self.Move(5, sheta2, 3)
                 self.Move(6, -sheta1-400,3)
                 self.Move(1, sheta3-450, 3)
                 self.Move(2, sheta2, 3)
                 self.Move(3, -sheta1-400, 3) 
                  
                 self.Move(7,  -250, 3) 
                 self.Move(8, 250, 3) 
                 self.Move(9,  sheta1+400, 3)
                 self.Move(10, -250, 3)
                 self.Move(11, 250, 3)
                 self.Move(12, sheta1+400, 3)
                 x-=0.3


    def CW(self):
            x = float(3.0)
            y = float(20.0)
            z = float(-155.0)
            for i in range(20):
                 sheta1, sheta2, sheta3 = Kinematics_f(x, y, z)
                 self.Move(1, sheta3-450, 3)
                 self.Move(2, sheta2, 3)
                 self.Move(3, sheta1-400, 3)
                 self.Move(4, sheta3-450, 3)
                 self.Move(5, sheta2, 3)
                 self.Move(6, sheta1-400, 3) 
                
                 self.Move(7, -250, 3)
                 self.Move(8, 250, 3)
                 self.Move(9, -sheta1+400, 3)
                 self.Move(10, -250, 3)
                 self.Move(11, 250, 3)
                 self.Move(12, -sheta1+400, 3)
                 x-= 0.3

            x = float(3.0)
            y = float(20.0)
            z = float(-155.0)
            for i in range(20):
                 sheta1, sheta2, sheta3 = Kinematics_f(x, y, z)
                 self.Move(10, -sheta3+450, 3)
                 self.Move(11, -sheta2, 3)
                 self.Move(12, sheta1+400, 3)
                 self.Move(7, -sheta3+450, 3)
                 self.Move(8, -sheta2, 3)
                 self.Move(9, sheta1+400, 3) 
                
                 self.Move(1, 250, 3)
                 self.Move(2, -250, 3)
                 self.Move(3, -sheta1-400, 3)
                 self.Move(4, 250, 3)
                 self.Move(5, -250, 3)
                 self.Move(6, -sheta1-400, 3)
                 x-= 0.3


    def Back(self):
            x = float(5.0)
            y = float(70.0)
            z = float(-165.0)
            for i in range(15):
                 sheta1, sheta2, sheta3 = Kinematics_f(x, y, z)
                 self.Move(1, sheta3-450, 0.1)
                 self.Move(2, sheta2, 0.1)
                 self.Move(3, -sheta1-450, 0.1)
                 self.Move(4, sheta3-450, 0.1)
                 self.Move(5, sheta2, 0.1)
                 self.Move(6, sheta1-450, 0.1) 
                
                 self.Move(7, -200, 0.1)
                 self.Move(8, 250, 0.1)
                 self.Move(9, -sheta1+450, 0.1)
                 self.Move(10, -200, 0.1)
                 self.Move(11, 250, 0.1)
                 self.Move(12, sheta1+450, 0.1)
                 self.Move(17, 0, 3)
                 self.Move(16, 1000, 3)
                 self.Move(15, 1000, 3)
                 x-= 1.0

            x = float(5.0)
            y = float(70.0)
            z = float(-165.0)
            for i in range(15):
                 sheta1, sheta2, sheta3 = Kinematics_f(x, y, z)
                 self.Move(10, -sheta3+450, 0.1)
                 self.Move(11, -sheta2, 0.1)
                 self.Move(12, -sheta1+450, 0.1)
                 self.Move(7, -sheta3+450, 0.1)
                 self.Move(8, -sheta2, 0.1)
                 self.Move(9, sheta1+450, 0.1) 
                
                 self.Move(1, 200, 0.1)
                 self.Move(2, -250, 0.1)
                 self.Move(3, sheta1-450, 0.1)
                 self.Move(4, 200, 0.1)
                 self.Move(5, -250, 0.1)
                 self.Move(6, -sheta1-450, 0.1)
                 self.Move(17, 0, 3)
                 self.Move(16, 1000, 3)
                 self.Move(15, 1000, 3)
                 x-= 1.0



    def Hill_Forward(self):
            x = float(14.0)
            y = float(65.0)
            z = float(-165.0)
            for i in range(40):
                 sheta1, sheta2, sheta3 = Kinematics_f(x, y, z)
                 self.Move(1, sheta3-450, 3)
                 self.Move(2, sheta2, 3)
                 self.Move(3, sheta1-450, 3)
                 self.Move(4, sheta3-450, 3)
                 self.Move(5, sheta2, 3)
                 self.Move(6, -sheta1-450, 3) 
                
                 self.Move(7, -750, 3)
                 self.Move(8, -450, 3)
                 self.Move(9, sheta1+250, 3)
                 self.Move(10, -250, 3)
                 self.Move(11, 250, 3)
                 self.Move(12, -sheta1+550, 3)
                 self.Move(17, 700, 1)
                 self.Move(16, -250, 1)
                 self.Move(15, 250, 1)
                 x-= 0.7
            self.Move(16, -100, 0.3)
            self.Move(17, -300, 0.3)
            self.Move(15, -100, 0.3)
            time.sleep(0.3)

            x = float(14.0)
            y = float(65.0)
            z = float(-165.0)
            for i in range(40):
                 sheta1, sheta2, sheta3 = Kinematics_f(x, y, z)
                 self.Move(10, -sheta3+450, 3)
                 self.Move(11, -sheta2, 3)
                 self.Move(12, sheta1+450, 3)
                 self.Move(7, -sheta3+450, 3)
                 self.Move(8, -sheta2, 3)
                 self.Move(9, -sheta1+450, 3) 
                
                 self.Move(1, 750, 3)
                 self.Move(2, 450, 3)
                 self.Move(3, -sheta1-250, 3)
                 self.Move(4, 250, 3)
                 self.Move(5, -250, 3)
                 self.Move(6, sheta1-550, 3)
                 self.Move(17, -700, 1)
                 self.Move(16, -250, 1)
                 self.Move(15, 250, 1)
                 x-= 0.7
            self.Move(16, -100, 0.3)
            self.Move(17, 300, 0.3)
            self.Move(15, -100, 0.3)
            time.sleep(0.3)


    def Hill_Back(self):
            x = float(2.0)
            y = float(10.0)
            z = float(-155.0)
            for i in range(40):
                 sheta1, sheta2, sheta3 = Kinematics_f(x, y, z)
                 self.Move(1, sheta3-450, 3)
                 self.Move(2, sheta2, 3)
                 self.Move(3, -sheta1-450, 3)
                 self.Move(4, sheta3-450, 3)
                 self.Move(5, sheta2, 3)
                 self.Move(6, sheta1-450, 3) 
                
                 self.Move(7, -250, 3)
                 self.Move(8, 300, 3)
                 self.Move(9, -sheta1+450, 3)
                 self.Move(10, -250, 3)
                 self.Move(11, 200, 3)
                 self.Move(12, sheta1+450, 3)
                 self.Move(17, 700, 1)
                 self.Move(16, -250, 1)
                 self.Move(15, -250, 1)
                 x-= 0.2
            self.Move(16, -00, 0.3)
            self.Move(17, -300, 0.3)
            self.Move(15, -100, 0.3)
            time.sleep(0.3)

            x = float(2.0)
            y = float(10.0)
            z = float(-155.0)
            for i in range(40):
                 sheta1, sheta2, sheta3 = Kinematics_f(x, y, z)
                 self.Move(10, -sheta3+450, 3)
                 self.Move(11, -sheta2, 3)
                 self.Move(12, -sheta1+450, 3)
                 self.Move(7, -sheta3+450, 3)
                 self.Move(8, -sheta2, 3)
                 self.Move(9, sheta1+450, 3) 
                
                 self.Move(1, 250, 3)
                 self.Move(2, -300, 3)
                 self.Move(3, sheta1-450, 3)
                 self.Move(4, 250, 3)
                 self.Move(5, -200, 3)
                 self.Move(6, -sheta1-450, 3)
                 self.Move(17, -700, 1)
                 self.Move(16, -250, 1)
                 self.Move(15, -250, 1)
                 x-= 0.2
            self.Move(16, -00, 0.3)
            self.Move(17, 300, 0.3)
            self.Move(15, -100, 0.3)
            time.sleep(0.3)


    def ball_get(self):      
             self.Move(13, -300, 50)
             self.Move(14, 300, 50)
             self.Move(1, 1100, 150)
             self.Move(2, 900, 150)
             self.Move(3, -100, 150)
             self.Move(4, 850, 150)
             self.Move(5, 500, 150)
             self.Move(6, -300, 150)
             self.Move(7, -1100, 150)
             self.Move(8, -900, 150)
             self.Move(9, 100, 150)
             self.Move(10, -850, 150)
             self.Move(11, -500, 150)
             self.Move(12, 300, 150)
             time.sleep(2)
             self.Move(13, 50, 50)
             self.Move(14, -50, 50)



    def ball_shoot(self):    
                     
             self.Move(1, 1100, 100)
             self.Move(2, 700, 100)
             self.Move(3, -300, 100)
             self.Move(4, -300, 100)
             self.Move(5, -800, 100)
            # Move(6, -300, 100)
             self.Move(7, -1100, 100)
             self.Move(8, -700, 100)
             self.Move(9, 300, 100)
             self.Move(10, 300, 100)
             self.Move(11, 800, 100)
            # Move(12, 300, 100)
             time.sleep(1)
                     
             self.Move(13, -100, 50)
             self.Move(14, 100, 50)
             time.sleep(1.5)
             self.Move(13,0, 50)
             self.Move(14, 0, 50)









if __name__ == "__main__":
    mode_class = Mode_C()
