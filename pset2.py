from Computation import Computation # from Computation.py
from ComputationalCell import FccCell # from ComputationalCell.py
from LennardJones import LennardJones # from LennardJones.py

from Vector3d import Vector3d
def make_computation():
	return Computation(CellType = FccCell, PotentialType = LennardJones)

def prob2():
	c = make_computation()
	e = c.energy_per_atom()
	print("energy per atom: ",e) # -6.0
	# note this value is invariant to L, M, N

	c.potential.r_c = 3
	e = c.energy_per_atom()
	print("r_c = 3, energy per atom: ",e) # -8.129

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

def prob5():
	c = make_computation()
	c.potential.r_c = 100
	c.computationalCell.vacancy = True
	c.minimize_energy_of_positions()
	# There's a bug in this one and it takes a really long time for the program to converge.
	# I'll try to straighten it out before the next assignment

def prob6():
	pass



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
	prob5()


