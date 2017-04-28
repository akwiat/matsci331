from Computation import Computation # from Computation.py
from ComputationalCell import FccCell # from ComputationalCell.py
from LennardJones import LennardJones # from LennardJones.py

from Vector3d import Vector3d
from Constants import kT_in_eV
import numpy as np

from Atom import Atom

def make_computation():
	return Computation(CellType = FccCell, PotentialType = LennardJones)

def prob1():
	# This is done inside the code for the ComputationalCell.
	# self.r_eq = 2**(1/6)
	# self.a = 2**(1/2) * self.r_eq
	pass

def prob2():
	c = make_computation()
	e = c.energy_per_atom()
	print("energy per atom: ",e) # -6.0
	# note this value is invariant to L, M, N
	# Since the coordination number of a fcc crystal is 12, and we're only considering nearest neighbors,
	# 6 is the value that we expect

	c.potential.r_c = 3
	e = c.energy_per_atom()
	print("r_c = 3, energy per atom: ",e) # -8.129
	# It's different because now long-range forces are taken into effect

def prob3():
	c = make_computation()
	force = c.force_on_atom()
	print("force: ",force) # 0, because all the atoms are at the equilibrium postiion

	# if you change the lattice constant, the atoms will no longer be at the equlibrium
	# positions, and there will be a non-zero restoring force.

def prob4():
	c = make_computation()
	e = c.total_energy()
	c.add_vacancy()
	e2 = c.total_energy()
	print("orig E: {}, after vacancy: {}, difference: {}".format(e,e2,e-e2))
	# orig E: -192.0, after vacancy: -180.0, difference: -12.0

	# 4. This makes sense because removing an atom breaks 12 bonds.
	# 5. 
	force = c.force_on_atom()
	print("force: ", force) # 0,0,0 because all the atoms are still at the eq positions

	c.potential.r_c = 3
	force = c.force_on_atom()
	print("force: {}, mag: {}".format(force, force.magnitude())) # mag: 0.03393682669038935

	for i in range(4):
		c.computationalCell.numBasic = i
		print("vacancy energy: {}".format(c.vacancy_energy()))

	# converged to -16.259018274544474

	# 7. with r_c = 3.0, longer range forces come into play, and atoms farther than just the nearest neighbors
	# will feel the force.

def prob5():
	c = make_computation()
	c.potential.r_c = 100
	c.computationalCell.vacancy = True
	c.minimize_energy_of_positions()
	# There's an issue with this one and it takes a really long time for the program to converge.
	# (Although nothing appears to be obviously wrong)
	# I'll try to straighten it out before the next assignment

	# To change the lattice vector:
	c.computationalCell.a *= 0.95
	c.minimize_energy_of_positions()

def prob6():
	# the given value of epsilon is equivalent to 0.0104 eV
	epsilon = 0.0104
	evac = 12
	exp_arg = -evac*epsilon/kT_in_eV(kelvin=20)
	print("exp_arg: ",exp_arg) # -72.4149936172682
	n = np.exp(exp_arg)
	print("n: ",n) # 3.5527763155e-32

	# in units of sigma, the lattice constant is:
	a = 2**(1/6)*2**(1/2)
	print("a: ", a) # 1.5874010519681996

	# the above concentration n is in units of a^3
	# so the concentration is 1 when (ka)^3 = 1/n
	k = ((1/n)**(1/3))/a
	print("k: {:.2e}".format(k)) # 1.92e+10
	# which is in units of sigma
	sigma = 3.4e-8
	print("size: (in cm)",k*sigma) # 651.532821108

	# 3. need to fix the code for part 5 first.

def prob7():
	# If alpha is too big, you can end up jumping back and forth across the true global min
	# If alpha is too small, it takes a very long time to reach the local min

	# Add an interstitial:
	c = make_computation()
	c.construct_full_atom_list()
	c.computationalCell.full_atom_list.append( Atom([0.5,0.5,0.5]) )
	c.minimize_energy_of_positions()
	# Also need to fix the code for part 5 to get this.

def test_potential():
	c = make_computation()
	p = c.potential
	# print(p.evaluate(2**(1/6)))
	print(p.eval_force(Vector3d([0,0,0.1])))

if __name__ == "__main__":
	# test_potential()
	# prob2()
	# prob3()
	# prob4()
	# prob5()
	prob6()


