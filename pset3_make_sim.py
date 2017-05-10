from ParticleSim import ParticleSim
from ComputationalCell import FccCell
from LennardJones import LennardJonesCts
from Verlet import Verlet
from Simulation import Simulation

import random

def Cell_pset3(temp=None, num_basic_copies=None):
	def make_cell():
		c = FccCell()
		c.numBasic = num_basic_copies
		c.initialize()
		# randomly initialize velocities
		c.randomize_velocities()
		c.scale_kinetic_energy_per_atom(temp)
		return c

	return make_cell

def make_sim(temp=0.2, num_basic_copies=1):
	random.seed(8484)
	computation = ParticleSim(CellType=Cell_pset3(temp=temp, num_basic_copies=num_basic_copies), PotentialType=LennardJonesCts, IntegrationType=Verlet)

	s = Simulation(computation=computation)
	s.num_steps = 1000
	s.deltat = 0.01
	# print([atom.v for atom in ps.computationalCell.full_atom_list])
	return s