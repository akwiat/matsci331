import numpy as np
from matplotlib import pyplot as plt
import json

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

		def to_JSON(self):
			return {
				"t":self.t,
				"q":self.q,
			}

		@classmethod
		def make_from_obj(cls, obj):
			ret = cls()
			ret.t = np.array(obj["t"])
			ret.q = np.array(obj["q"])
			return ret

	def __init__(self, computation=None):
		self.tracked_quantities = {}
		self.num_steps = 100
		self.deltat = None
		self.t = 0.0
		self.computation = computation

		self.should_plot = False
		self.should_store = True

		self.name = None

	def track_quantity(self, computeFn, name=None):
		if name is None:
			name is str(len(self.tracked_quantities))

		tq = self.TrackedQuantity(computeFn)
		tq.setup(num_steps=self.num_steps)
		self.tracked_quantities[name] = tq

	def propagate(self):
		for name,tq in self.tracked_quantities.items():
			d = tq.compute()
			# print("recording: ",d)
			tq.record(self.t, d)

	def plot(self):
		for name,tq in self.tracked_quantities.items():
			plt.figure()
			# print(tq.t)
			# print(tq.q)
			plt.plot(tq.t, tq.q)
		plt.show()

	def make_storage_name(self, tqname):
		if self.name is None:
			raise ValueError("no simulation name")
		if tqname is None:
			raise ValueError("no tracked quantity name")

		return "{}_{}".format(self.name, tqname)

	def store(self):
		for name, tq in self.tracked_quantities.items():
			with open(self.make_storage_name(name), "w") as f:
				json.dump(tq.to_JSON(), f)

	def post_run(self):
		if self.should_plot is True:
			self.plot()
		if self.should_store is True:
			self.store()

	def run(self):
		for step in range(self.num_steps):
			step = round(self.t/self.deltat)
			if step % 100 == 0:
				print("*********Step: ",step)

			self.propagate()
			self.computation.propagate(deltat=self.deltat)
			self.t += self.deltat
		self.post_run()

	def plot_file(self, filename):
		with open(filename) as f:
			obj = json.load(f)

		tq = self.TrackedQuantity.make_from_obj(obj)
		plt.figure()
		plt.plot(tq.t, tq.q)
		plt.show()
