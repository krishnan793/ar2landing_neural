#!/usr/bin/env python

# This node is used to capture training data.
# https://github.com/krishnan793/ar2landing_neural
# Author : Ananthakrishnan U S

import rospkg
import rospy
import message_filters
import numpy as np
from visualization_msgs.msg import Marker
from geometry_msgs.msg import TwistStamped

def callback(data,twist_data):
	#print data.header.seq,
	#print data.pose.position.z
	#reading = Twist()
	#reading = rospy.wait_for_message("/cmd_vel", Twist)
	MAX = 2
	if (twist_data.twist.linear.x !=0 or twist_data.twist.linear.z !=0 or twist_data.twist.angular.z !=0 or twist_data.twist.linear.y !=0 ):
		x1 = normalize(data.pose.position.x,MAX)
		x2 = normalize(data.pose.position.y,MAX)
		x3 = normalize(data.pose.position.z,MAX)
		x4 = normalize(data.pose.orientation.x,MAX)
		x5 = normalize(data.pose.orientation.y,MAX)
		x6 = normalize(twist_data.twist.linear.x,MAX)
		x7 = normalize(twist_data.twist.linear.y,MAX)
		x8 = normalize(twist_data.twist.linear.z,MAX)
		x9 = normalize(twist_data.twist.angular.z,MAX)
		msg = str(format(x1, '.3f'))+" "+str(format(x2, '.3f'))+" "+str(format(x3, '.3f'))+" "+str(format(x4, '.3f'))+" "+str(format(x5, '.3f'))+" "+str(format(x6, '.3f'))+" "+str(format(x7, '.3f'))+" "+str(format(x8, '.3f'))+" "+str(format(x9, '.3f'))+"\n"
		print data.header.seq
		print data.pose.position.z
		#rospy.loginfo(rospy.get_caller_id() + "I heard %s", msg)
		f.write(msg)

def normalize(data,MAX):
	return (data+1)/MAX
def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
	
	rospy.init_node('NNtrainer', anonymous=True)
	filter0 = message_filters.Subscriber('/visualization_marker', Marker)
	filter1 = message_filters.Subscriber('/cmd_vel_header', TwistStamped)
	ts = message_filters.ApproximateTimeSynchronizer([filter0, filter1],10,1)
	ts.registerCallback(callback)
	#pub2 = rospy.Subscriber("/visualization_marker", Marker, callback)

	rospy.spin()

if __name__ == '__main__':
	# get an instance of RosPack with the default search paths
	rospack = rospkg.RosPack()

	# get the file path for rospy_tutorials
	path = rospack.get_path('ar2landing_gazebo')
	f = open(path+'/data/data.txt','a+')
	listener()

