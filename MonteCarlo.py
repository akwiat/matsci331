import random
import numpy as np

from Computation import Computation

class MonteCarlo(Computation):
	def __init__(self, CellType=None, PotentialType=None, temp=None):
		super.__init__(CellType=CellType, PotentialType=PotentialType)
		self.beta = 1/temp if temp else None # the MC temp

	def sample_atom(self):
		atom_list = self.computationalCell.explicit_atom_list
		return random.choice(atom_list)

	def propagate(self, deltat=None):
		orig_energy = self.total_potential_energy()

		atom = self.sample_atom()
		# adjust one atom
		randvec = atom.r.random()
		half = randvec.id() * 0.5
		print("rand: ", randvec)
		delta = self.delta_scale * (randvec - half)
		print("delta: ", delta)
		atom.r += delta

		# compute energy
		energy = self.total_potential_energy()

		# decide whether to keep the change (based on beta)
		delta_energy = energy - orig_energy
		cutoff = np.exp(-self.beta * delta_energy)
		sample = random.random()
		if sample < cutoff:
			#keep the change
			pass
		else:
			atom.r -= delta
			# undo the change