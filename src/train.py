#!/usr/bin/env python

# This node will train the network.
# https://github.com/krishnan793/ar2landing_neural
# Author : Ananthakrishnan U S

import rospkg
import time
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(num):
	return 1.0/(1+np.exp(-1*num))
def sigmoid_h(num):
	return np.tanh((num/2)/2+0.5)

# get an instance of RosPack with the default search paths
rospack = rospkg.RosPack()

# get the file path for rospy_tutorials
path = rospack.get_path('ar2landing_neural')

data = np.loadtxt(path+"/data/data.txt")
# X = 4x3 mxn
# Y = 4x1 oxp




Y_n = 4	# No of outputs
X = data[:,:-1*Y_n]
Y = data[:,-1*Y_n:]
X = X / 1#X.max(axis=0)
Y = Y / 1#Y.max(axis=0)
X = np.insert(X,0,1,axis=1)
[m, n] = X.shape
[o, p] = Y.shape
# ----------------
print "Data",data
print "X:",X
print "X:",X.shape
print "Y:",Y.shape

#-----------------

w1 = 2*np.random.random((n,4)) - 1
w2 = 2*np.random.random((4,p)) - 1

#-----------------

#print "w1",w1.shape
#print "w2",w2.shape

iteration = 100000

error =[float("inf")]
plt.ion()
plt.show()
for i in range(iteration):
	l1 = sigmoid(np.dot(X,w1))
	l2 = sigmoid(np.dot(l1,w2))

	l2_error = Y - l2
	l2_delta = l2_error * l2 * (1-l2) *.01

	l1_error = np.dot(l2_delta,w2.T)
	tmp = l1*(1-l1)
	l1_delta = l1_error*tmp*.01
	#---------------------

	w2 += np.dot(l1.T,l2_delta)
	w1 += np.dot(X.T,l1_delta)
	tmp = np.sum(l2_error**2,axis=0)
	tmp = np.sum(tmp,axis=0)
	error.append(tmp)
	#---------------------
	if(i%200==0):
		plt.scatter(i, tmp)
		plt.draw()
		print error[i+1]
		#if(abs(error[i]-error[i+1])<0.001):
		#	break
	

np.set_printoptions(precision=2)

np.savez(path+"/data/weights.npz",w1,w2)

