import random
import numpy as np

from Computation import Computation

class MonteCarlo(Computation):
	class AnnealingSchedule:
		def __init__(self, start=None, end=None, num_steps=None):
			self.start = start
			self.val = self.start
			self.end = end
			self.max_steps = num_steps
			self.delta = (end-start)/num_steps
			self.num_steps = 0

		def propagate(self):
			self.val += self.delta
			self.num_steps += 1
			if self.num_steps >= self.max_steps:
				self.val = self.end

			if self.val < 0.001: self.val = 0.001
			return self.val


	def __init__(self, CellType=None, PotentialType=None, temp=None):
		super().__init__(CellType=CellType, PotentialType=PotentialType)
		self.beta = 1/temp if temp else None # the MC temp

		self.total_attempts = 0
		self.num_accepts = 0
		self.delta_scale = 0.1

		self.burn = 1000

		self.annealing_schedule = None

	def prepare(self):
		for i in range(self.burn):
			self.propagate()
		print("Burned in: {} steps".format(self.burn))

	def sample_atom(self):

		atoms_list = self.atoms_list
		return random.choice(atoms_list)

	def percentage_accepts(self):
		if self.total_attempts == 0: return 0
		return self.num_accepts/self.total_attempts


	def propagate(self, deltat=None):
		# print("old energy")
		orig_energy = self.total_potential_energy()

		atom = self.sample_atom()
		# adjust one atom
		randvec = atom.r.random()
		half = randvec.identity() * 0.5
		# print("rand: ", randvec)
		delta = self.delta_scale * (randvec - half)
		# print("delta: ", delta)
		atom.r += delta

		# compute energy
		self.cache["total_potential"] = None
		# print("new energy")
		energy = self.total_potential_energy()

		# decide whether to keep the change (based on beta)
		delta_energy = energy - orig_energy
		# print("delta_e: ", delta_energy)
		cutoff = np.exp(-self.beta * delta_energy)
		# print("delta: ",delta_energy, " cutoff: {}".format(cutoff))
		sample = random.random()
		if sample < cutoff:
			#keep the change
			self.num_accepts += 1
			# print("accepting: ", self.num_accepts)
		else:
			atom.r -= delta
			self.cache["total_potential"] = orig_energy
			# undo the change
			# print("rejecting")
		self.total_attempts += 1

		if self.annealing_schedule is not None:
			temp = self.annealing_schedule.propagate()
			self.beta = 1/temp

