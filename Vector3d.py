import numpy as np

class Vector3d(np.ndarray):
	def __init__(self, buffer):
		super.__init__(shape=(3,1), order='F', buffer=buffer)

	def magnitude(self):
		return np.linalg.norm(self)
