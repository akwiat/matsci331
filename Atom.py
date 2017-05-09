
from Vector3d import Vector3d

class Atom:
	def __init__(self, arr=None):
		self.r = Vector3d(arr)
		self.v = Vector3d()
		self.mass = 1

	def translate_clone(self, origin):
		ret = Atom()
		ret.r = self.r + origin
		ret.v = self.v
		ret.mass = self.mass
		return ret

	def kinetic_energy(self):
		return self.v.square()