
def kT_in_eV(kelvin=300):
	return 8.617e-5 * kelvin

class Units:
	def __init__(self):
		self.epsilon = 167e-16 * 1e-7
		self.sigma = 3.4e-10

		self.amu_to_kg = 1.66e-27
		self.mass = 40 * self.amu_to_kg

		self.hbar = 1e-34

	def time_true_units(self, timesteps):
		return timesteps * self.mass**(1/2)*self.sigma * self.epsilon**(-1/2)

	def distance_true_units(self, r):
		pass
