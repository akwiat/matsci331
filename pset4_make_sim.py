import random

from ParticleSim import ParticleSim
from ComputationalCell import FccCell
from LennardJones import LennardJonesCts
from Verlet import Verlet
from Simulation import Simulation

from MonteCarlo import MonteCarlo


def Cell_pset4(temp=None, num_basic_copies=None):
	def make_cell():
		c = FccCell()
		c.numBasic = num_basic_copies
		c.initialize()
		# randomly initialize velocities
		c.randomize_velocities()
		c.scale_kinetic_energy_per_atom(temp)
		return c

	return make_cell

def make_md(temp=0.2, num_basic_copies=1):
	random.seed(8484)
	computation = ParticleSim(CellType=Cell_pset4(temp=temp, num_basic_copies=num_basic_copies), PotentialType=LennardJonesCts, IntegrationType=Verlet)
	computation.setup_optimization()
	s = Simulation(computation=computation)
	s.num_steps = 1000
	s.deltat = 0.01
	# print([atom.v for atom in ps.computationalCell.full_atom_list])
	return s

def make_montecarlo(temp=0.2, num_basic_copies=1):
	random.seed(8484)
	computation = MonteCarlo(CellType=Cell_pset4(temp=temp, num_basic_copies=num_basic_copies), PotentialType=LennardJonesCts, temp=temp)
	computation.setup_optimization()
	s = Simulation(computation=computation)
	s.num_steps = 1000
	s.deltat = 1
	return s