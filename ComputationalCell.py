from LennardJones import LennardJones
from Atom import Atom
from Vector3d import Vector3d
import random

class ComputationalCell:
	def __init__(self):
		# self.numAtoms = 10
		self.numBasic = 1
		# maxCompCells = 1
		# self.L = numBasic
		# self.M = numBasic	
		# self.N = numBasic
		self.atoms = []
		self.a = None
		self.vacancy = False

		self.full_atom_list = []
		self.use_explicit_list = False

		# self.construct_full_atom_list()

	def construct_full_atom_list(self):
		self.use_explicit_list = True
		numBasic = self.numBasic
		for l in range(numBasic):
			for m in range(numBasic):
				for n in range(numBasic):
					for ai, a in enumerate(self.atoms):
						nOrigin = self.a * Vector3d([l,m,n])
						nAtom = a.translate_clone(nOrigin)
						self.full_atom_list.append(nAtom)

		if self.vacancy:
			self.full_atom_list.pop()

		print("list size: ",len(self.full_atom_list))
		return self.full_atom_list

	def cell_size(self):
		if self.a is None:
			raise ValueError
		return self.a * self.numBasic

	def num_atoms(self):
		if self.use_explicit_list:
			return len(self.full_atom_list)
		else:
			return len(self.atoms) * self.numBasic**3

	def iter_atoms(self):
		if self.use_explicit_list:
			for a in self.full_atom_list:
				yield a
			return
		else:
			numBasic = self.numBasic
			for l in range(numBasic):
				for m in range(numBasic):
					for n in range(numBasic):
						for ai, a in enumerate(self.atoms):

							if self.vacancy:
								if l==0 and m==0 and n==0:
									if ai==1:
										continue

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

	def total_kinetic_energy(self):
		result = 0.0
		for atom in self.iter_atoms():
			result += atom.v.square()

		return result

	def randomize_velocities(self):
		for atom in self.iter_atoms():
			atom.v = Vector3d([random.uniform(-1,1) for i in range(3)])

	def scale_kinetic_energy(self, desired_ke):
		total_ke = self.total_kinetic_energy()
		# print("total_ke: ",total_ke)
		scalefactor = (desired_ke/total_ke)**(0.5)

		for atom in self.iter_atoms():
			atom.v *= scalefactor
			# print(atom.v)

	def scale_kinetic_energy_per_atom(self, energy_per_atom):
		total_energy = energy_per_atom*self.num_atoms()
		self.scale_kinetic_energy(total_energy)

class FccCell(ComputationalCell):
	def __init__(self):
		super().__init__()
		self.atoms.append(Atom([0,0,0]))
		self.atoms.append(Atom([0,1,1]))
		self.atoms.append(Atom([1,1,0]))
		self.atoms.append(Atom([1,0,1]))
		self.r_eq = 2**(1/6)
		self.rescale() # eq r
		self.construct_full_atom_list()

	def rescale(self):
		scaleFactor = self.r_eq/2**(1/2)
		self.a = 2**(1/2) * self.r_eq
		# print("a: {}".format(self.a))
		for a in self.atoms:
			a.r = a.r*scaleFactor
			# print(a.r, a.r.magnitude())


