#!/usr/bin/env python 

import roslib
import rospy
import math

PI = math.pi

def Kinematics_f(x, y, z):  
    sheta1rad = float(math.atan2(x, y))
    sheta1 = float((sheta1rad* 180.0 / PI)*10)

    C3 = float(((x-pow(51.2*math.sin(sheta1rad),2) + pow(y - 51.2*math.cos(sheta1rad),2) + pow(z,2)-pow(54.2,2)-pow(118.0,2)) /(2*54.2*118.0)))
    sheta3rad = float(math.atan2(math.sqrt(1-pow(C3,2)),C3))
    sheta3 = float((sheta3rad*180.0 / PI)*10)

    k = float(-math.sqrt(pow(x-math.sin(sheta1rad)*51.2,2)) + pow(y-math.cos(sheta1rad)*51.2,2    ))
    g = float(-(pow(math.sin(sheta3rad),2)*pow(118.0,2))-pow(math.cos(sheta3rad)*118.0 + 54.2,2    ))
    a = float(math.cos(sheta3rad)*118.0+54.2)
    
    sheta2rad = float(math.atan2(((k*math.sin(sheta3rad)*118.0)-a*z)/g,(-k*a-(math.sin(sheta3rad)*118.0*z))/g))
    sheta2 = float((sheta2rad*180.0 / PI)*10)
    
    return sheta1, sheta2, sheta3

if __name__ == '__main__':
    pass
