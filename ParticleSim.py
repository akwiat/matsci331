from Computation import Computation
from Verlet import Verlet

class ParticleSim(Computation):
	def __init__(self):
		self.computational_cell = None
		self.integration_method = Verlet()
		self.cur_t = 0.0

	def acc_of_atom(atom):
		f = self.computational_cell.force_on_atom(atom):
		a = f/atom.mass

	def propagate(steps=1000, deltat=0.01):
		atoms = self.computational_cell.iter_atoms
		for atom in atoms:
			self.integration_method.integrate(atom=atom, deltat=deltat, get_acc=self.acc_of_atom)
			
