from LennardJones import LennardJones
from Atom import Atom
from Vector3d import Vector3d

class ComputationalCell:
	def __init__(self):
		# self.numAtoms = 10
		self.numBasic = 2
		# maxCompCells = 1
		# self.L = numBasic
		# self.M = numBasic	
		# self.N = numBasic
		self.atoms = []
		self.a = None
		self.vacancies = []

	def cell_size(self):
		if self.a is None:
			raise ValueError
		return self.a * self.numBasic
	def iter_atoms(self):
		numBasic = self.numBasic
		for l in range(numBasic):
			for m in range(numBasic):
				for n in range(numBasic):
					for a in self.atoms:
						nOrigin = self.a * Vector3d([l,m,n])
						yield a.translate_clone(nOrigin)
		return

	def compute_potential(self):
		result = 0
		for i, ai in enumerate(self.atoms):
			for j, aj in enumerate(self.atoms):
				for l in range(-self.lmax, self.lmax):
					for m in range(-self.mmax, self.mmax):
						for n in range(-self.nmax, self.nmax):
							if i == j and l == m == n:
								continue
							rVector = ai.r - aj.r
							r = rVector.magnitude()
							result += self.potential.evaluate(r)

		return result

	def compute_force(self):
		r_0 = Vector3d()
		result = Vector3d()
		for i, ai in enumerate(self.atoms):
			for l in range(-self.lmax, self.lmax):
				for m in range(-self.mmax, self.mmax):
					for n in range(-self.nmax, self.nmax):
						relative = ai.r - r_0
						f = self.potential.eval_force(relative)
						result += f

class FccCell(ComputationalCell):
	def __init__(self):
		super().__init__()
		self.atoms.append(Atom([0,0,0]))
		self.atoms.append(Atom([0,1,1]))
		self.atoms.append(Atom([1,1,0]))
		self.atoms.append(Atom([1,0,1]))
		self.r_eq = 2**(1/6)
		self.rescale() # eq r

	def rescale(self):
		scaleFactor = self.r_eq/2**(1/2)
		self.a = 2**(1/2) * self.r_eq
		# print("a: {}".format(self.a))
		for a in self.atoms:
			a.r = a.r*scaleFactor
			# print(a.r, a.r.magnitude())


