#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32

class jejee(object):
    def __init__(self):
        self.pub = rospy.Publisher("/chan_yagi", Int32, queue_size = "1")
        self.sub = rospy.Subscriber("/yagi", Int32, self.callback)
    def callback(self, data):
        y = data.data
        print("kite")
        n = 1
        self.pub.publish(n)


if __name__ == "__main__":
    rospy.init_node("mode_pub")
    J = jejee()
    rospy.spin()

