from pset3_make_sim import make_sim

from Constants import Units

def test_verlet():

    sim = make_sim(num_basic_copies=1)
    # sim.track_quantity(sim.computation.total_energy)
    # print("total ke: ",sim.computation.total_kinetic_energy())
    sim.track_quantity(sim.computation.temperature)
    sim.num_steps = 100
    sim.run()
    # sim.plot()
    # ps.potential.plot_potential()
    # ps.potential.plot_force()
    # ps.propagate()
    # ps.energy_per_atom()

def prob2():
    stepsizes = [0.01, 0.02, 0.04, 0.06]
    for stepsize in stepsizes:
        sim = make_sim(num_basic_copies=1) # This should be num_basic_copies = 2, but it takes too long
        sim.track_quantity(sim.computation.temperature)
        sim.track_quantity(sim.computation.total_energy_deviation)
        sim.num_steps = 100 # Should be 1000, but it takes too long
        sim.deltat = stepsize
        sim.run()

def prob3():
    def iteration(num_basic_copies):
        sim = make_sim(num_basic_copies=num_basic_copies)
        sim.num_steps = 2000
        sim.deltat = 0.01

    # numcopies = [1,2,3] # This is what I should do, but it takes too long
    numcopies = [1]
    for num_basic_copies in numcopies:
        iteration(num_basic_copies)



def prob5():
    # Based on previous simulations, the approximate period of one atomic oscillation is:
    period = 0.1 # in units of 'time step', which is m**(1/2) * sigma / epsilon**(1/2)
    units = Units()
    units.epsilon = 1
    true_time = units.time_true_units(period)
    true_freq = 1/true_time
    energy = true_freq * units.hbar

    print("energy: ", energy) # In units of epsilon = 1
    # Compare to kbT = 0.2



def prob6():
    def mean_sq_disp(temp=None):
        sim = make_sim(temp=temp, num_basic_copies=3)
        sim.deltat = 0.01
        sim.num_steps = 2000
        sim.track_quantity(sim.computation.mean_squared_displacement)
        sim.run()

    temps = [0.2, 4]
    for temp in temps:
        mean_sq_disp(temp=temp)



if __name__ == "__main__":
    test_verlet()
    prob2()

