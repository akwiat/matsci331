from ParticleSim import ParticleSim
from ComputationalCell import FccCell
from LennardJones import LennardJonesCts
from Verlet import Verlet

def make_sim():
	ps = ParticleSim(CellType=FccCell, PotentialType=LennardJonesCts, IntegrationType=Verlet)
	return ps

def test_verlet:
	ps = make_sim()
	ps.propagate()

if __name__ == "__main__":
	test_verlet()