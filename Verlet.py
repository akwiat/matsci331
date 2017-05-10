
class Verlet:
	def __init__(self):
		pass

	def integrate(self, atom=None, deltat=None, get_acc=None):
		# print("-----Verlet: ")
		# print("atom.r: ", atom.r)
		# print("atom.v: ", atom.v)
		# print("after: ")
		a_0 = get_acc(atom)
		# print("acc: ", a_0)

		v = atom.v
		deltar = v*deltat + 0.5*a_0*deltat**2
		# print("deltar: ", deltar)
		atom.r += deltar

		a_t = get_acc(atom)
		
		# print("vel: ", v, " acc: ",a_0, " a_t: ",a_t)
		deltav = 0.5*(a_0 + a_t)*deltat
		atom.v += deltav
		# print("atom.r: ", atom.r)
		# print("atom.v: ", atom.v)
		# print("\n")
		return atom

	def initialize(self, computation, deltat=None):
		pass

class RegularVerlet:
	def __init__(self):
		self.acc_fn = None

	def initialize(self, computation, deltat=None):
		for atom in computation.iter_atoms():
			if atom.integration_data is None: atom.integration_data = {}
			atom.integration_data["oldr"] = atom.r.clone()
			a_0 = self.acc_fn(atom)
			deltar = atom.v*deltat + 0.5*a_0 * (deltat**2)
			atom.r += deltar

	def integrate(self, atom=None, deltat=None):
		r = atom.r
		rold = atom.integration_data["oldr"]
		a = self.acc_fn(atom)

		rnew = 2*r - rold + a*(deltat**2)

		atom.integration_data["oldr"] = atom.r
		atom.r = rnew
		


