import numpy as np
from matplotlib import pyplot as plt
import json
import shutil
import os

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

		def np_write_file(self, filename):
			np.save(filename, np.vstack([self.t, self.q]))

		@classmethod
		def np_load(cls, filename):
			ret = cls(None)
			arr = np.load(filename)
			l = np.vsplit(arr, 2)
			ret.t = l[0][0]
			ret.q = l[1][0]
			# print(ret.t)
			# print(ret.q)
			return ret

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
		self.should_store = False
		self.should_write = True

		self.name = None

	def track_quantity(self, computeFn, name=None):
		if name is None:
			name is str(len(self.tracked_quantities))
			print("warning - no name chosen for tracked_quantity")

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

		return os.path.join(self.name, "{}.npy".format(tqname))

	def store(self):
		for name, tq in self.tracked_quantities.items():
			filename = self.make_storage_name(name)
			tq.np_write_file(filename)

	def post_run(self):
		if self.should_plot is True:
			self.plot()
		if self.should_store is True:
			self.store()
		if self.should_write is True:
			self.write_file()

	def run(self):
		for step in range(self.num_steps):
			step = round(self.t/self.deltat)
			if step % 100 == 0:
				print("*********Step: ",step)

			self.propagate()
			self.computation.propagate(deltat=self.deltat)
			self.t += self.deltat
		self.post_run()

	def make_file_name(self):
		if self.name is None: raise ValueError("no simulation name")
		return os.path.join(self.name, "{}.sim".format(self.name))

	def write_file(self):
		tqnamelist = []
		if self.name is None: raise ValueError("no simulation name")
		if os.path.exists(self.name):
			shutil.rmtree(self.name)
		os.mkdir(self.name)
		for name, tq in self.tracked_quantities.items():
			filename = self.make_storage_name(name)
			tq.np_write_file(filename)
			tqnamelist.append(filename)
		with open(self.make_file_name(), "w") as f:
			json.dump(tqnamelist, f)

	@classmethod
	def make_from_file(cls, name):
		ret = cls()
		ret.name = name
		with open(ret.make_file_name()) as f:
			tqnamelist = json.load(f)

		for name in tqnamelist:
			ret.tracked_quantities[name] = cls.TrackedQuantity.np_load(name)
		return ret

	def plot_file(self, filename):
		with open(filename) as f:
			obj = json.load(f)

		tq = self.TrackedQuantity.make_from_obj(obj)
		plt.figure()
		plt.plot(tq.t, tq.q)
		plt.show()
