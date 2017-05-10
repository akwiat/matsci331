import numpy as np
from matplotlib import pyplot as plt

class Simulation:
	class TrackedQuantity:
		def __init__(self, compute):
			self.t = None
			self.q = None
			self.compute = compute #fn that accepts the computation and returns a scalar
			self.cur_index = 0

		def setup(self, num_steps=None):
			self.t = np.zeros(num_steps)
			self.q = np.zeros(num_steps)

		def record(self, time, data):
			self.t[self.cur_index] = time
			self.q[self.cur_index] = data
			self.cur_index += 1

	def __init__(self, computation=None):
		self.tracked_quantities = []
		self.num_steps = 100
		self.deltat = None
		self.t = 0.0
		self.computation = computation

	def track_quantity(self, computeFn):
		tq = self.TrackedQuantity(computeFn)
		tq.setup(num_steps=self.num_steps)
		self.tracked_quantities.append(tq)

	def propagate(self):
		for tq in self.tracked_quantities:
			d = tq.compute()
			# print("recording: ",d)
			tq.record(self.t, d)

	def plot(self):
		for tq in self.tracked_quantities:
			plt.figure()
			plt.plot(tq.t, tq.q)
		plt.show()

	def run(self):
		for step in range(self.num_steps):
			# print("*********Step: ",self.t/self.deltat)
			self.propagate()
			self.computation.propagate(deltat=self.deltat)
			self.t += self.deltat
		self.plot()
