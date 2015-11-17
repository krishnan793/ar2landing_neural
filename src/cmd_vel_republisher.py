#!/usr/bin/env python
# This node will republish cmd_vel with header data. This is for capturing training data.
# https://github.com/krishnan793/ar2landing_neural
# Author : Ananthakrishnan U S

import rospkg
import rospy

from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import Twist

def callback(data):
	data_new = TwistStamped()
	data_new.header.stamp = rospy.Time.now()
	data_new.twist = data
	pub2.publish(data_new)

def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
	
	rospy.init_node('cmd_vel_republisher', anonymous=True)
	pub1 = rospy.Subscriber("/cmd_vel", Twist, callback)

	rospy.spin()

if __name__ == '__main__':
	# get an instance of RosPack with the default search paths
	rospack = rospkg.RosPack()
	pub2 = rospy.Publisher('/cmd_vel_header', TwistStamped, queue_size=10)
	listener()

