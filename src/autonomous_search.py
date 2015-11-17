#!/usr/bin/env python

# This node will perform a lawn mower search pattern unti a tag is detected
# https://github.com/krishnan793/ar2landing_neural
# Author : Ananthakrishnan U S

import roslib
# ardrone_tutorials has a good ardrone classs for controlling drone. load_manifest import that python module
roslib.load_manifest("ardrone_control")

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from visualization_msgs.msg import Marker
from drone_controller import BasicDroneController
import time



def detect_tag(data):
	# This will set a flag and stop executing autonomous search
	controller.SetCommand(0,0,0,0)
	controller.StopSendCommand()
	global detect
	detect = 1

def sleep(sec):
	while(sec and not rospy.is_shutdown()):
		if(detect==1):
			break
		time.sleep(1)
		sec -= 1

def reset():
	nothing = Empty()
	print nothing
	pub = rospy.Publisher('/ardrone/reset', Empty, queue_size=10)
	time.sleep(1)
	pub.publish(nothing)
	return

def reset_drone(pub1):
	controller.SetCommand(0,0,0,0)
	time.sleep(1)

def search_pattern():
	controller.SetCommand(0,0,0,1.5)
	sleep(5)
	controller.SetCommand(0,0,0,0)
	sleep(1)
	while not rospy.is_shutdown() and detect == 0:
		controller.SetCommand(0,1,0,0)
		sleep(1)
		controller.SetCommand(-1,0,0,0)
		sleep(9)
		controller.SetCommand(0,1,0,0)
		sleep(1)
		controller.SetCommand(1,0,0,0)
		sleep(9)	
if __name__ == '__main__':
	rospy.init_node('autonomous_search', anonymous=True)
	pub1 = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	controller = BasicDroneController()
	controller.StartSendCommand()
	time.sleep(1)
	detect = 0
	controller.SendTakeoff()
	controller.StartSendCommand()
	pub2 = rospy.Subscriber("/visualization_marker", Marker, detect_tag)
	search_pattern()
	reset_drone(pub1)
	rospy.spin()


