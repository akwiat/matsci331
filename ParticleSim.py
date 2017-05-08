from Computation import Computation

class ParticleSim(Computation):
	def __init__(self, CellType=None, PotentialType=None, IntegrationType=None):
		super().__init__(CellType=CellType, PotentialType=PotentialType)
		self.integration_method = IntegrationType()
		self.cur_t = 0.0

	def acc_of_atom(self, atom):
		f = self.force_on_atom(atom)
		a = f/atom.mass
		return a

	def propagate(self, steps=1000, deltat=0.01):
		atoms = self.iter_atoms()
		for atom in atoms:
			# print(atom.v)
			self.integration_method.integrate(atom=atom, deltat=deltat, get_acc=self.acc_of_atom)
			
