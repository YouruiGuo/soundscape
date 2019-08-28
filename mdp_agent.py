import numpy as np
import math
import sys, os
from env import Environment
import threading
import time
from virtualsubject import Subject
import numpy.random as rnd

class Agent(object):
	"""docstring for Agent"""
	def __init__(self):
		super(Agent, self).__init__()
		#self.arg = arg
		self.actions = [-1, 0, 1]
		self.env = Environment()
		self.is_undo = False
		self.accumulative_reward = 0
		self.range = [0,1,2,3,4,5,6,7,8,9,10]
		self.rangelen = len(self.range)-1
		self.state_action_value = np.zeros((self.rangelen**self.env.n, len(self.actions)*self.env.n))
		self.alpha = 0.7
		self.gamma = 1


	def agent_start(self):
		#print(self.env.curr_state)
		curr_state = self.env.curr_state
		self.num = self.env.n
		self.action_values = np.zeros(shape=(self.num,len(self.actions)))
		self.action_nums = np.zeros(shape=(self.num,len(self.actions)))
		stepsize = 0.1
		n = np.random.randint(self.num)
		action = [n, stepsize * self.actions[np.random.randint(3)]]
		self.prev_action = action
		self.prev_state = curr_state
		return action, curr_state

	def agent_step(self, r):
		prev_sn = self.state_to_num(self.prev_state)
		prev_an = self.action_to_num(self.prev_action)
		curr_state = self.env.curr_state
		curr_sn = self.state_to_num(curr_state)
		
		self.state_action_value[prev_sn][prev_an] += self.alpha * \
			(r + self.gamma * np.max(self.state_action_value[curr_sn]) - self.state_action_value[prev_sn][prev_an])
		

		stepsize = self.getStepSize(r)
		epsilon = rnd.uniform()
		if (epsilon < 0.2):
			n = np.random.randint(self.num)
			ac = stepsize * self.actions[np.random.randint(3)]
			#print(n, ac)
			action = [n, ac]
		else:
			a = np.argmax(self.state_action_value[curr_sn])
			action = [int(a/len(self.actions)), 0.01 * self.actions[a%len(self.actions)]]
		
		self.prev_action = action
		self.prev_state = curr_state
		return action, curr_state

	def getStepSize(self, r):
		return 0.1

	def inrange(self, num):
		for i in range(self.rangelen):
			if num >= self.range[i] and num < self.range[i+1]:
				return self.range[i]


	def state_to_num(self, state):
		#print(state)
		num = 0
		for i in range(len(state)-1):
			#print(state[i]['vol'])
			num += self.inrange(state[i]['vol'])
			num *= 10
		#print(state[len(state)-1]['vol'])
		num += self.inrange(state[len(state)-1]['vol'])

		return int(num)

	def action_to_num(self, action):
		return int(action[0]*len(self.actions) + int(np.sign(action[1])))


def no_response():
	global act, st, reward, steps, start_time
	global th, vsub
	t = time.time() - start_time
	steps += 1
	if steps > 10000:
		print("accumulative_reward",agt.accumulative_reward)
		quit()
	else:
		#print("****************************", steps)
		th = threading.Timer(0.001, no_response)
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
	global root, th, agt, vsub
	print("accumulative_reward",agt.accumulative_reward)
	print("vector:", agt.env.curr_state)
	print("goal:", vsub.goal_vec)
	distance = 0
	for i in range(agt.env.n):
		distance += (vsub.goal_vec[i]['vol'] - agt.env.curr_state[i]['vol'])**2
	distance = math.sqrt(distance)
	print("distance", distance)
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
