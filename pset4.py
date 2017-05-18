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

if __name__ == "__main__":
    # test_montecarlo()
    # test_md()
    test_storage()

