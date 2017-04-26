import numpy as np
from Vector3d import Vector3d

class LennardJones:
	def __init__(self, sigma=1, epsilon=1, r_c=1.3):
		self.sigma = sigma
		self.epsilon = epsilon
		self.r_c = r_c

	def evaluate(self, r):
		if r >= self.r_c:
			return 0
		else:
			rs = self.sigma/r
			# print("r: {}".format(r))
			return 4*self.epsilon*(rs**12 - rs**6)

	def gradientMag(self, r):
		rs = self.sigma/r
		return 4*self.epsilon*(12*rs**11 - 6*rs**5)*(-rs/r)

	def eval_force(self, rVector):
		# print("eval_force: rVector: ",rVector)
		r = np.linalg.norm(rVector)
		if r >= self.r_c:
			return Vector3d()
		g = self.gradientMag(r)
		rhat = rVector/r
		result = rhat * -g # force is negative gradient
		# print("eval_force: result: ",result)
		return result

