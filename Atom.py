
from Vector3d import Vector3d

class Atom:
	def __init__(self, arr):
		self.r = Vector3d(arr)

	def translate_clone(self, origin):
		ret = Atom(0)
		ret.r = self.r + origin
		return ret