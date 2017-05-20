from Vector3d import Vector3d
from Atom import Atom

import types
import math

class Computation:
	class Cache(dict):
		def __init__():
			super().__init__()

		def invalidate(name):
			self[name] = None


	def __init__(self, CellType=None, PotentialType=None):
		self.CellType = CellType
		self.computationalCell = CellType()
		self.numCopies = 3
		# self.a = 1
		self.potential = PotentialType()


		self.initial_energy = None

		self.optimize_iter_atoms = False

		self.cache = {}

	def setup_optimization(self):
		self.all_atoms_list = []
		for atom in self.iter_all_atoms():
			self.all_atoms_list.append(atom)

		self.atoms_list = []
		for atom in self.iter_atoms():
			self.atoms_list.append(atom)

		self.cell_list = []
		for cell in self.iter_cells():
			self.cell_list.append(cell)

		def return_explicit_list(self):
			return self.atoms_list

		def explicit_all_atoms(self):
			return self.all_atoms_list

		def explicit_cells(self):
			return self.cell_list

		self.iter_atoms = types.MethodType(return_explicit_list, self)
		self.iter_cells = types.MethodType(explicit_cells, self)
		# Computation.iter_all_atoms = explicit_all_atoms

		self.optimize_iter_atoms = True

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
		num_middle = (numCopies-1)/2

		for x in range(numCopies):
			for y in range(numCopies):
				for z in range(numCopies):
					xm = x - num_middle
					ym = y - num_middle
					zm = z - num_middle
					nOrigin = cell_size * Vector3d([xm, ym, zm])
					yield (self.computationalCell, nOrigin)
		return

	def get_cell_origin(self, x, y, z):
		cell_size = self.computationalCell.cell_size()
		nOrigin = cell_size * Vector3d([x,y,z])
		return nOrigin

	def iter_all_atoms(self, _retatom=Atom()):
		for cell,origin in self.iter_cells():
			for a in cell.iter_atoms():
				nAtom = a.translate_clone(origin)
				yield nAtom
				# a.clone_to(_retatom)
				# _retatom.r += origin
				# yield _retatom
		return

	# def iter_atoms(self):
	# 	cell = self.computationalCell
	# 	num_middle = (self.numCopies-1)/2
	# 	origin = self.get_cell_origin(num_middle, num_middle, num_middle)

	# 	for a in cell.iter_atoms():
	# 		nAtom = a.translate_clone(origin)
	# 		yield nAtom
	# 	return

	def iter_atoms(self):
		for a in self.computationalCell.iter_atoms():
			yield a
		return

	def store_initial_positions(self):
		self.initial_atoms = []
		for atom in self.iter_atoms():
			self.initial_atoms.append(atom.clone())

	def num_atoms(self):
		return self.computationalCell.num_atoms()

	def mean_squared_displacement(self):
		result = 0.0
		for ai, a in zip(self.initial_atoms, self.iter_atoms()):
			dif = a.r - ai.r
			result += dif.square()

		return result/self.num_atoms()

	def total_energy_deviation(self):
		if self.initial_energy is None:
			self.initial_energy = self.total_energy()

		total = self.total_energy()
		dev = total - self.initial_energy
		return dev/(3*self.num_atoms())

	def total_energy(self):
		result = 0.0
		for ai in self.iter_atoms():
			ke = ai.kinetic_energy()
			# print("ke: ",ke)
			result += ke
			result += self.potential_of_atom(ai)
		return result				

	def potential_of_atom(self, atom):
		result = 0.0
		for aj in self.iter_all_atoms():
			rVector = atom.r - aj.r
			r = rVector.magnitude()
			if r < 0.0001: continue
			contribution = self.potential.evaluate(r)
			result += contribution
		return result

	def total_kinetic_energy(self):
		result = 0
		for atom in self.iter_atoms():
			result += atom.kinetic_energy()
		return result

	def temperature(self):
		ke = self.total_kinetic_energy()
		return ke/self.num_atoms()

	def total_potential_energy(self):
		if "total_potential" in self.cache:
			cache_val = self.cache["total_potential"]
			# print(cache_val)
			if cache_val is not None:
				# print("using cache")
				return cache_val

		result = 0
		count = 0
		bondcount = 0
		inner_loop_count = 0
		full_atom_list = []
		for atom in self.iter_all_atoms():
			full_atom_list.append(atom)

		for ai in self.iter_atoms():
			# count += 1
			for aj in full_atom_list:
			# for aj in self.iter_all_atoms():
				# rVector = ai.r - aj.r
				# r = rVector.magnitude()
				
				r = math.sqrt((ai.r[0] - aj.r[0])**2 + (ai.r[1] - aj.r[1])**2 + (ai.r[2] - aj.r[2])**2)
				# print((ai.r[0] - aj.r[0])**2 + (ai.r[1] - aj.r[1])**2 + (ai.r[2] - aj.r[2])**2)
				
				if r < 0.001: continue

				result += self.potential.evaluate(r)
				# result += contribution


		# self.num_atoms = count
		# print("bondcount: {}".format(bondcount))
		final_result = result/2

		self.cache["total_potential"] = final_result
		# print("caching: ", final_result)
		# print(inner_loop_count)
		return final_result

	def force_on_atom(self, atom=None):
		if atom is None:
			nOrigin = self.get_cell_origin(1,1,1)
			atom = self.computationalCell.atoms[0]
			atom = atom.translate_clone(nOrigin)

		force = Vector3d()
		# for a in self.iter_atoms():
		for a in self.iter_all_atoms():
			# print("force_on_atom::a.r: ", a.r)
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

	def potential_per_atom(self):
		result = self.total_potential_energy()/self.num_atoms
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



