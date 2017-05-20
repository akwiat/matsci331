import numpy as np
import random
from numpy.linalg import norm as norm
import math

class Vector3d(np.ndarray):
	def __new__(cls, buffer=[0.0,0.0,0.0]):
		# super().__new__(shape=(3,1), order='F', buffer=buffer)
		obj = np.asarray(buffer).view(cls)
		return obj

	def clone(self):
		return Vector3d(np.copy(self))

	def magnitude(self):
		return math.sqrt(self[0]**2 + self[1]**2 + self[2]**2)
		# return np.linalg.norm(self)

	def square(self):
		return self.magnitude()**2

	def normalize(self):
		m = self.magnitude()
		if m == 0:
			raise ValueError

		return self / m

	@classmethod
	def random(cls):
		ret = cls([random.random() for i in range(3)])
		return ret

	@classmethod
	def identity(cls):
		ret = cls([1]*3)
		return ret
