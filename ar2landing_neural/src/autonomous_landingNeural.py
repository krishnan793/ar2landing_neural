#!/usr/bin/env python

# This node will perform autonomous landing using neural network.
# https://github.com/krishnan793/ar2landing_neural
# Author : Ananthakrishnan U S

import roslib
roslib.load_manifest("ardrone_control")

import rospkg
import rospy
import time
import message_filters
import numpy as np
from std_msgs.msg import Empty
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist
from visualization_msgs.msg import Marker
from drone_controller import BasicDroneController

def land():
	controller.SendLand()
	rospy.loginfo(rospy.get_caller_id() + " Quad copter Landed")
	time.sleep(1)
	return

def sigmoid(num):
	return 1.0/(1+np.exp(-1*num))

def normalize(data,MAX):
	return (data+1)/MAX
	
def callback(data):
	if(controller.commandTimer==None):
		controller.StartSendCommand()
	x1 = normalize(data.pose.position.x,MAX)
	x2 = normalize(data.pose.position.y,MAX)
	x3 = normalize(data.pose.position.z,MAX)
	x4 = normalize(data.pose.orientation.x,MAX)
	x5 = normalize(data.pose.orientation.y,MAX)
	
	if(x3<=0.55):
		land()
		rospy.signal_shutdown("Landed")
		
	X=[1,x1,x2,x3,x4,x5]

	Y=sigmoid(np.dot(X,w1))
	Z=sigmoid(np.dot(Y,w2))
	Z=np.around(Z, decimals=2)
	rospy.loginfo(rospy.get_caller_id() + " Input  %s %s %s %s %s", format(x1, '.2f'),format(x2, '.2f'),format(x3, '.2f'),format(x4, '.2f'),format(x5, '.2f'))
	control(Z)

def load_weights(file):
	fp=np.load(file)
	w1=fp['arr_0']
	w2=fp['arr_1']
	#print w1
	#print w2
	return [w1,w2]
	
def control(Z):
	cntrl = Twist()
	x=2*Z[0]-1
	y=2*Z[1]-1
	z=2*Z[2]-1
	angz=2*Z[3]-1
	rospy.loginfo(rospy.get_caller_id() + " Output %s %s %s %s", x,y,z,angz)
	controller.SetCommand(y,x,angz,z)

def limit_reading(data,MAX):
	if(data>MAX):
		data=MAX
	return data
def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
	
	rospy.Subscriber("/visualization_marker", Marker, callback)
	rospy.spin()

if __name__ == '__main__':
	# get an instance of RosPack with the default search paths
	rospack = rospkg.RosPack()
	
	path = rospack.get_path('ar2landing_neural')
	rospy.init_node('NNcontroller', anonymous=True)
	MAX = 2
	[w1,w2]=load_weights(path+"/data/weights.npz")
	controller = BasicDroneController()
	listener()

