from ParticleSim import ParticleSim
from ComputationalCell import FccCell
from LennardJones import LennardJonesCts
from Verlet import Verlet
from Simulation import Simulation

import random

def Cell_pset3():
	c = FccCell()
	# randomly initialize velocities
	c.randomize_velocities()
	c.scale_kinetic_energy_per_atom(0.002)
	return c

def make_sim():
	computation = ParticleSim(CellType=Cell_pset3, PotentialType=LennardJonesCts, IntegrationType=Verlet)

	s = Simulation(computation=computation)
	s.num_steps = 100
	s.deltat = 0.001
	# print([atom.v for atom in ps.computationalCell.full_atom_list])
	return s

def test_verlet():

	sim = make_sim()
	# sim.track_quantity(sim.computation.total_energy)
	print("total ke: ",sim.computation.total_kinetic_energy())
	sim.track_quantity(sim.computation.total_energy)
	sim.run()
	# sim.plot()
	# ps.potential.plot_potential()
	# ps.potential.plot_force()
	# ps.propagate()
	# ps.energy_per_atom()

if __name__ == "__main__":
	random.seed(8484)
	test_verlet()