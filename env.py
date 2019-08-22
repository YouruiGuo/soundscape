import numpy as np
import math
from collections import defaultdict
#from control import Control
from pythonosc import udp_client

def sigmoid(x):
  return 1 / (1 + math.exp(-0.1*x))


class Environment(object):
	"""docstring for Environment"""
	def __init__(self):
		#super(Environment, self).__init__()
		#self.arg = arg
		self.env_init()

	def randomVolume(self):
		""" 
			generate random volume, 1 decimal 
			volume range: 0 - 10
		"""
		# mean: 3, variance: 2
		a = 2 * np.random.randn() + 3
		if a < 0:
			a = 0
		if a > 10:
			a = 10
		return round(a, 1)
	'''
	def goal(self):
		for i in range(self.n):
			self.goal_soundscape[i]['vol'] = self.randomVolume()
	'''
	def createSoundscape(self):
		""" 
			Create Soundscape
			n: number of sounds
			self.soundscape: dictionary
		"""
		self.env_soundscape = []
		#self.goal_soundscape = []
		self.stateActionValue = defaultdict(list)
		self.n = 2
		for i in range(self.n):
			self.env_soundscape.append(defaultdict(list)) 
			#self.goal_soundscape.append(defaultdict(list)) 
		

	def env_init(self):
		self.createSoundscape()
		#self.goal()
		self.Q = 0
		self.feedback = np.random.rand()
		self.gamma = 1
		self.alpha = 0.7
		self.curr_state = 0
		self.next_state = 0
		self.reward = 0
		#self.ctl = Control(self.n)
		for i in range(self.n):
			# random number [0, 10), 1 decimal
			self.env_soundscape[i]['vol'] = round(np.random.rand()*10, 1)
		#self.ctl.set_init_volume(self.env_soundscape[:]['vol'])
		print(self.env_soundscape)
		#print(self.goal_soundscape)
	
	def isGoal(self, total_reward):
		if abs(1 - total_reward) <= 0.01:
			return True
		else:
			return False
	
	def biofeedback(self, a, res, t):

		send_action(a)

		self.getNextState(a)
		'''
		if res == None:
			self.reward = math.tanh(t)
		else:
			self.reward = -1
		'''
		self.reward = res


		self.next_state = self.env_soundscape

		#reward = self.next_state - self.curr_state
		#self.reward = 1.0 / (1.0 + self.next_state)
		#self.reward += 0.1 * (noise - 0.3)
		self.Q = (1 - self.alpha) * self.Q + self.alpha * self.reward


	def getNextState(self, a):
		#print(a)
		self.env_soundscape[a[0]]['vol'] += a[1]

	def updateStateActionValue(self, a, s, res, t):

		self.biofeedback(a, res, t)
	
		r = self.Q
		#print("reward: ", r)
		#print(self.env_soundscape)
		if self.isGoal(r):
			return float('inf')
		self.curr_state = self.next_state
		return r


def send_action(act):
	#print(act)
	client = udp_client.SimpleUDPClient("127.0.0.1", 57120) #default ip and port for SC
	client.send_message("/print", act) # set the frequency at 440