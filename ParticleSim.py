from Computation import Computation
from Simulation import Simulation

class ParticleSim(Computation):
	def __init__(self, CellType=None, PotentialType=None, IntegrationType=None):
		super().__init__(CellType=CellType, PotentialType=PotentialType)
		self.integration_method = IntegrationType()
		self.cur_t = 0.0
		self.simulation = None

		self.integration_method.acc_fn = self.acc_of_atom
		self.integration_method.initialize(self)

	def acc_of_atom(self, atom):
		f = self.force_on_atom(atom)
		a = f/atom.mass
		return -a


	def propagate(self, deltat=None):
		self.cached_all_atoms = None # invalidate cache every iteration
		for atom in self.iter_atoms():
			# print(atom.v)
			self.integration_method.integrate(atom=atom, deltat=deltat, get_acc=self.acc_of_atom)
			
