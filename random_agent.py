import numpy as np
import math
import sys, os
from env import Environment
import threading
import time
from virtualsubject import Subject

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
		stepsize = self.getStepSize(r)
		
		n = np.random.randint(self.num)
		ac = 0.01 * self.actions[np.random.randint(3)]
		#print(n, ac)
		action = [n, ac]
		self.prev_action = action
		return action, curr_state

	def getStepSize(self, r):
		return 0.01

def no_response():
	global act, st, reward, steps, start_time
	global th, vsub
	t = time.time() - start_time
	steps += 1
	if steps > 100000:
		print("accumulative_reward",agt.accumulative_reward)
		quit()
	#print("****************************", steps)
	th = threading.Timer(0.0001, no_response)
	th.start()
	#a = scale.get()
	res = vsub.getreward(agt.env.env_soundscape)

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


def quit():
	global root, th, agt
	print("accumulative_reward",agt.accumulative_reward)
	th.cancel()
	#root.destroy()

def main():
	global act, st, agt, steps, start_time
	global vsub
	vsub = Subject()

	start_time = time.time()
	steps = 0
	agt = Agent()
	act, st = agt.agent_start()
	#print(act, st)
	vsub.init(agt.env)

	no_response()

if __name__ == '__main__':
	main()




	#-68093.69191840113