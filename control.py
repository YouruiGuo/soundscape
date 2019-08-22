import OSC
import time, random

class Control(object):
	"""docstring for Control"""
	def __init__(self, n):
		self.num = n
		self.src = ['1.mp3', '2.mp3']

	def set_init_volume(self, vec):
		pass

	def volume(self, vec):
		pass
		
	def play_sound(self):
