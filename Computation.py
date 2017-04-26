from Vector3d import Vector3d

class Computation:
	def __init__(self, CellType=None, PotentialType=None):
		self.computationalCell = CellType()
		self.numCopies = 1
		# self.a = 1
		self.potential = PotentialType()


	def iter_cells(self): # (cell, origin)
		cell_size = self.computationalCell.cell_size()
		numCopies = self.numCopies

		for x in range(numCopies):
			for y in range(numCopies):
				for z in range(numCopies):
					nOrigin = cell_size * Vector3d([x, y, z])
					yield (self.computationalCell, nOrigin)
		return

	def iter_atoms(self):
		for cell,origin in self.iter_cells():
			for a in cell.iter_atoms():
				nAtom = a.translate_clone(origin)
				yield nAtom
		return

	def total_energy(self):
		result = 0
		count = 0
		for ai in self.iter_atoms():
			count += 1
			for aj in self.iter_atoms():
				rVector = ai.r - aj.r
				if rVector.magnitude() < 0.001: continue
				r = rVector.magnitude()
				# print(r)
				result += self.potential.evaluate(r)
		self.num_atoms = count

		return result/2

	def energy_per_atom(self):
		result = self.total_energy()/self.num_atoms
		print("num_atoms: {}".format(self.num_atoms))
		return result

