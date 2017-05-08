from ParticleSim import ParticleSim
from ComputationalCell import FccCell
from LennardJones import LennardJonesCts
from Verlet import Verlet
import random

def Cell_pset3():
	c = FccCell()
	# randomly initialize velocities
	c.randomize_velocities()
	c.scale_kinetic_energy_per_atom(1.5)
	return c

def make_sim():
	ps = ParticleSim(CellType=Cell_pset3, PotentialType=LennardJonesCts, IntegrationType=Verlet)
	print([atom.v for atom in ps.computationalCell.full_atom_list])
	return ps

def test_verlet():
	ps = make_sim()
	ps.propagate()

if __name__ == "__main__":
	random.seed(8484)
	test_verlet()