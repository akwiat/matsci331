from Computation import Computation
from ComputationalCell import FccCell
from LennardJones import LennardJones

def make_computation():
	return Computation(CellType = FccCell, PotentialType = LennardJones)
def prob2():
	c = make_computation()
	# totalE = c.total_energy()
	# print(totalE)
	e = c.energy_per_atom()
	print(e)

def prob3():
	c = make_computation()
	force = c.force_on_atom()
	print("force: ",force)


def test_potential():
	c = make_computation()
	p = c.potential
	print(p.evaluate(2**(1/6)))

if __name__ == "__main__":
	# test_potential()
	# prob2()
	prob3()