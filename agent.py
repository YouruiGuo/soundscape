import numpy as np
import math
import sys, os
from env import Environment
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
import threading
import time
from virtualsubject import Subject
from tkinter import *


class Agent(object):
	"""docstring for Agent"""
	def __init__(self):
		super(Agent, self).__init__()
		#self.arg = arg
		self.actions = [-1, 0, 1]
		self.env = Environment()
		self.is_undo = False
		self.accumulative_reward = 0
		
		
	def agent_start(self):
		curr_state = self.env.curr_state
		self.num = self.env.n
		self.action_values = np.zeros(shape=(self.num,len(self.actions)))
		self.action_nums = np.zeros(shape=(self.num,len(self.actions)))
		stepsize = 0.01
		n = np.random.randint(self.num)
		action = [n, stepsize * self.actions[np.random.randint(3)]]
		self.prev_action = action
		return action, curr_state

	def agent_step(self, r):
		curr_state = self.env.curr_state
		action = []
		stepsize = self.getStepSize(r)
		a1 = self.signOfNumber(self.prev_action[1]) + 1
		avl = self.action_values[self.prev_action[0]][a1]
		self.action_nums[self.prev_action[0]][a1] += 1
		self.action_values[self.prev_action[0]][a1] =\
								avl + (r - avl) / self.action_nums[self.prev_action[0]][a1]
		#if r == -1:
		#	action = self.undo()
		#	self.is_undo = True
		#else:
		epsilon = np.random.rand()
		if (epsilon < 0.1):
			#self.is_undo = False
			n = np.random.randint(self.num)
			ac = stepsize * self.actions[np.random.randint(3)]
			action = [n, ac]
			#print(action)
		else:
			#action = self.prev_action
			ind = np.unravel_index(np.argmax(self.action_values, axis=None), self.action_values.shape)
			#print("index:  ", ind )
			action = [int(ind[0]), float(self.actions[ind[1]]*stepsize)]
			#self.is_undo = False
		#print("action", action)
		#print(self.action_values)
		self.prev_action = action
		#send_actions(action)
		return action, curr_state


	def signOfNumber(self, num):
		return int(np.sign(num))

	def undo(self):
		#print("undo")
		action = [self.prev_action[0], -1*self.prev_action[1]]
		#self.prev_action = action
		return action


	def getStepSize(self, r):
		return 0.01

'''
def set_filter(address, *args):
	#print("new")
	global act, st, reward, steps, start_time
	start_time = time.time()
	steps += 1
	if abs(args[0]) < 0.00001:
		sys.exit()
	reward = agt.env.updateStateActionValue(act, st, -1, 0)
	if reward == float('inf'):
		print("steps:", steps)
		sys.exit()  
	act, st = agt.agent_step(reward)


def default_handler(address, *args):
    #print("DEFAULT", address, args)
    sys.exit() 

def userFeedback(user_input):
	global client
	ip = "127.0.0.1"
	port = 6448
	client = SimpleUDPClient(ip, port)  # Create client

	# spawn a new thread to wait for input 
	def get_user_input():
		while True:
		    #user_input = input()
		    #user_input = np.random.randint(11)
		    client.send_message("/wek/inputs", float(user_input))

	mythread = threading.Thread(target=get_user_input, args=())
	mythread.daemon = True
	mythread.start()
'''

def no_response():
	global act, st, reward, steps, start_time, client, scale
	global th, vsub
	t = time.time() - start_time
	steps += 1
	if steps > 100000:
		quit()
	#print("****************************", steps)
	th = threading.Timer(0.0001, no_response)
	th.start()
	#a = scale.get()
	res = vsub.getreward(agt.env.env_soundscape)
	#print(res)
	reward = agt.env.updateStateActionValue(act, st, res, t)
	agt.accumulative_reward += reward
	# end of episode, reached the goal
	if reward == float('inf'):
		#th.cancel()
		#threading.enumerate()
		print("steps: ", steps)
		quit()
		
		#client.send_message("/wek/inputs", float(0))
	act, st = agt.agent_step(reward)


def sel():
	selection = "Value = " + str(var.get())
	label.config(text = selection)


def quit():
	global root, th, agt
	print(agt.accumulative_reward)
	th.cancel()
	#root.destroy()

def main():
	
	global steps, act, st, agt, dispatcher, start_time, server, scale, root
	global vsub
	vsub = Subject()

	start_time = time.time()
	steps = 0
	agt = Agent()
	act, st = agt.agent_start()
	vsub.init(agt.env)
	'''
	# slider gui
	root = Tk()
	var = DoubleVar()
	scale = Scale( root, from_=0, to=10, length=300,tickinterval=1, orient=HORIZONTAL) 
	#scale = Scale( root, variable = var, orient=HORIZONTAL, command=show_values )
	scale.pack(anchor=CENTER)

	label = Label(root)
	label.pack()
	'''
	#userFeedback(scale.get())
	no_response()
	#root.mainloop()
	#os._exit(0)
	'''
	# communicate with wekinator
	dispatcher = Dispatcher()
	dispatcher.map("/wek/outputs", set_filter)
	dispatcher.set_default_handler(default_handler)

	ip = "127.0.0.1"
	port = 12000

	server = BlockingOSCUDPServer((ip, port), dispatcher)
	server.serve_forever()  # Blocks forever
	'''

if __name__ == '__main__':
	main()

	#-101422.57142857142