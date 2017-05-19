from pset4_make_sim import make_md, make_montecarlo

def test_montecarlo():

    sim = make_montecarlo(num_basic_copies=1, temp=0.1)
    sim.num_steps = 100
    sim.track_quantity(sim.computation.percentage_accepts)
    sim.track_quantity(sim.computation.total_potential_energy)
    sim.run()

def test_md():
    sim = make_md(num_basic_copies=1, temp=0.2)
    sim.num_steps = 100
    sim.track_quantity(sim.computation.total_potential_energy)
    sim.run()

def test_storage():
    sim = make_md(num_basic_copies=1, temp=0.2)
    sim.name = "storagetest"
    sim.num_steps = 10
    sim.track_quantity(sim.computation.total_potential_energy, name="total_energy")
    sim.run()

def test_loading():
    sim = make_md()
    sim = sim.make_from_file("storagetest")
    sim.plot()

def prob1():
    sim = make_md(num_basic_copies=2, temp=0.2)
    sim.name = "p1_heatcapacity"
    sim.deltat = 0.01
    sim.num_steps = 100 * 2
    sim.track_quantity(sim.computation.temperature, "temp")
    sim.run()

def prob1_display():
    sim = make_md()
    sim = sim.make_from_file("p1_heatcapacity")
    sim.plot()

if __name__ == "__main__":
    # test_montecarlo()
    # test_md()
    # test_storage()
    # test_loading()
    # prob1()
    prob1_display()

