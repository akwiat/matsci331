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

def test_potential():
	c = make_computation()
	p = c.potential
	print(p.evaluate(0.7))

if __name__ == "__main__":
	# test_potential()
	prob2()