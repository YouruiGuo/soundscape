import numpy as np
import math
from collections import defaultdict

class Subject(object):
	"""docstring for Subject"""
	def __init__(self):
		self.reward_range = range(10)
		self.goal_vec = []

	def init(self, env):
		self.n = env.n
		for i in range(self.n):
			self.goal_vec.append(defaultdict(list))
		self.distribution()

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

	def distribution(self):
		for x in range(self.n):
			self.goal_vec[x]['vol'] =  self.randomVolume()

	def distance(self, dist):
		#return math.exp(-0.1*dist)-1
		if dist > 10:
			return -1
		else:
			return -0.2 * (dist - 5)

	def getreward(self, env_vec):
		distance = 0
		#print(self.goal_vec)
		#print(env_vec)
		for i in range(self.n):
			distance += (self.goal_vec[i]['vol'] - env_vec[i]['vol'])**2
		distance = math.sqrt(distance)


		dist = self.distance(distance) 
		#print("distance", distance)
		#if (distance > 5):
		#	return -1 + 0.3 * diff
		#	return -1
		#else:
		#	return 0.7 * (-0.2 * (distance - 5)) + 0.3 * diff
		#	return -0.2 * (distance - 5)
		return dist
