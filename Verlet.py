
class Verlet:
	def __init__(self):
		pass

	def integrate(self, atom=None, deltat=None, get_acc=None):
		# print("-----Verlet: ")
		# print("atom.r: ", atom.r)
		# print("atom.v: ", atom.v)
		# print("after: ")
		a_0 = get_acc(atom)
		# print("acc: ", a_0)

		v = atom.v
		deltar = v*deltat + 0.5*a_0*deltat**2
		# print("deltar: ", deltar)
		atom.r += deltar

		a_t = get_acc(atom)
		print("vel: ", v, " acc: ",a_0, " a_t: ",a_t)
		deltav = 0.5*(a_0 + a_t)*deltat
		atom.v += deltav
		# print("atom.r: ", atom.r)
		# print("atom.v: ", atom.v)
		# print("\n")
		return atom