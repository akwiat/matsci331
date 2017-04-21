from lennard-jones import LennardJones

class ComputationalCell:
	def __init__(self):
		self.numAtoms = 10
		self.L = 3
		self.M = 3
		self.N = 3
		self.lmax = 3
		self.mmax = 3
		self.nmax = 3
		self.atoms = []
		self.potential = LennardJones()

	def computePotential(self):
		result = 0
		for i, ai in enumerate(self.atoms):
			for j, aj in enumerate(self.atoms):
				for l in range(-self.lmax, self.lmax):
					for m in range(-self.mmax, self.mmax):
						for n in range(-self.nmax, self.nmax):
							rVector = ai.r - aj.r
							r = rVector.magnitude()
							result += self.potential.evaluate(r)

		return result

	def computeForce(self):
		r_0 = Vector3d()
		result = Vector3d()
		for i, ai in enumerate(self.atoms):
			for l in range(-self.lmax, self.lmax):
				for m in range(-self.mmax, self.mmax):
					for n in range(-self.nmax, self.nmax):
						relative = ai.r - r_0
						f = self.potential.eval_force(relative)
						result += f