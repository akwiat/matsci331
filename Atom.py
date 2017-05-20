
from Vector3d import Vector3d

class Atom:
	def __init__(self, arr=None):
		self.r = Vector3d(arr)
		self.v = Vector3d()
		self.mass = 1
		self.integration_data = None

	def clone(self):
		ret = Atom()
		ret.r = self.r.clone()
		ret.v = self.v.clone()
		ret.mass = self.mass
		# ret.integration_data = self.integration_data
		return ret

	def translate_clone(self, origin):
		ret = self.clone()
		ret.r += origin
		return ret

	def clone_to(self, atom):
		atom.r = self.r.clone()
		return atom



	def kinetic_energy(self):
		return self.v.square()