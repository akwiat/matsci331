from Vector3d import Vector3d

class Computation:
	def __init__(self, CellType=None, PotentialType=None):
		self.CellType = CellType
		self.computationalCell = CellType()
		self.numCopies = 3
		# self.a = 1
		self.potential = PotentialType()


	def add_vacancy(self):
		self.computationalCell.vacancy = True

	def vacancy_energy(self):
		self.computationalCell.vacancy = False
		e = self.total_energy()
		self.computationalCell.vacancy = True
		e2 = self.total_energy()
		return e-e2

	def iter_cells(self): # (cell, origin)
		cell_size = self.computationalCell.cell_size()
		numCopies = self.numCopies

		for x in range(numCopies):
			for y in range(numCopies):
				for z in range(numCopies):
					nOrigin = cell_size * Vector3d([x, y, z])
					yield (self.computationalCell, nOrigin)
		return

	def get_cell_origin(self, x, y, z):
		cell_size = self.computationalCell.cell_size()
		nOrigin = cell_size * Vector3d([x,y,z])
		return nOrigin

	def iter_atoms(self):
		for cell,origin in self.iter_cells():
			for a in cell.iter_atoms():
				nAtom = a.translate_clone(origin)
				yield nAtom
		return

	def iter_main_cell_atoms(self):
		cell = self.computationalCell
		num_middle = (self.numCopies-1)/2
		origin = self.get_cell_origin(num_middle, num_middle, num_middle)

		for a in cell.iter_atoms():
			nAtom = a.translate_clone(origin)
			yield nAtom
		return

	def total_energy(self):
		result = 0
		count = 0
		bondcount = 0
		for ai in self.iter_main_cell_atoms():
			count += 1
			for aj in self.iter_atoms():
				rVector = ai.r - aj.r
				if rVector.magnitude() < 0.001: continue
				r = rVector.magnitude()
				# print(r)
				contribution = self.potential.evaluate(r)
				if contribution < -0.5:
					bondcount += 1
				result += contribution
				# print(contribution)
				# print(result)
		self.num_atoms = count
		print("bondcount: {}".format(bondcount))
		return result/2

	def force_on_atom(self, atom=None):
		if atom is None:
			nOrigin = self.get_cell_origin(1,1,1)
			atom = self.computationalCell.atoms[0]
			atom = atom.translate_clone(nOrigin)

		force = Vector3d()
		for a in self.iter_atoms():
			rVector = a.r - atom.r
			if rVector.magnitude() < 0.001: continue
			force_contribution = self.potential.eval_force(rVector)
			# print(force_contribution)
			force += force_contribution
			force_mag = force.magnitude()
			if force_mag > 1000:
				print(a.r)
				print(atom.r)
				print(rVector.magnitude(), force, force_contribution)
				raise ValueError
		return force

	def energy_per_atom(self):
		result = self.total_energy()/self.num_atoms
		print("num_atoms: {}".format(self.num_atoms))
		return result

	def grad_step_iteration(self):
		alpha = 0.005

		max_force = 0
		total_force = 0
		count = 0
		for a in self.computationalCell.full_atom_list:
			# print(a.r)
			count += 1
			force = self.force_on_atom(a)
			adjust = force*alpha
			# print("adjust: ",adjust)
			# print("r: ",a.r)
			a.r = a.r - adjust
			# a.r = a.r - force.normalize()*alpha

			force_mag = force.magnitude()
			if force_mag > max_force:
				max_force = force_mag
			total_force += force_mag

		avg_force = total_force/count
		print("avg_force: ", avg_force)
		return max_force
	def minimize_energy_of_positions(self):
		tolerance = 0.01
		self.computationalCell.construct_full_atom_list()
		count = 0
		while True:
			# print(self.computationalCell.full_atom_list[1].r)
			max_force = self.grad_step_iteration()
			count += 1
			print("max_force size: ",max_force)
			if max_force < tolerance:
				break
			total_energy = self.total_energy()
			print("total_energy: ",total_energy)



