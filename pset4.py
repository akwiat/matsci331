from pset4_make_sim import make_md, make_montecarlo

def test_montecarlo():

    sim = make_montecarlo(num_basic_copies=1, temp=0.1)
    sim.track_quantity(sim.computation.total_potential_energy)
    sim.num_steps = 100
    sim.run()


if __name__ == "__main__":
    test_montecarlo()

