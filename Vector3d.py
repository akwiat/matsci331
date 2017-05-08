import numpy as np

class Vector3d(np.ndarray):
	def __new__(cls, buffer=[0.0,0.0,0.0]):
		# super().__new__(shape=(3,1), order='F', buffer=buffer)
		obj = np.asarray(buffer).view(cls)
		return obj

	def magnitude(self):
		return np.linalg.norm(self)

	def square(self):
		return self.magnitude()**2
		
	def normalize(self):
		m = self.magnitude()
		if m == 0:
			raise ValueError

		return self / m
