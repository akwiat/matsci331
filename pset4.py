from pset4_make_sim import make_md, make_montecarlo, make_nanoparticle_montecarlo
import cProfile


def test_montecarlo():

    sim = make_montecarlo(num_basic_copies=2, temp=0.1)
    sim.num_steps = 200
    sim.track_quantity(sim.computation.percentage_accepts)
    # sim.track_quantity(sim.computation.total_potential_energy)
    sim.should_plot = True
    sim.run()

def test_md():
    sim = make_md(num_basic_copies=2, temp=0.2)
    sim.num_steps = 100
    sim.should_plot = True
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
    sim = make_md(num_basic_copies=1, temp=0.2)
    sim.name = "p1_heatcapacity"
    sim.deltat = 0.01
    sim.num_steps = 100 * 2
    sim.track_quantity(sim.computation.temperature, "temp")
    sim.run()

def prob1_highT():
    sim = make_md(num_basic_copies=2, temp=4)
    sim.name = "p1_heatcapacity_highT"
    sim.deltat = 0.01
    sim.num_steps = 100 * 2
    sim.track_quantity(sim.computation.temperature, "temp")
    sim.run()

def prob1_display():
    sim = make_md()
    sim = sim.make_from_file("p1_heatcapacity")
    sim.plot()

def test_total_potential():
    sim = make_montecarlo(num_basic_copies=2, temp=0.1)
    for i in range(100):
        sim.computation.total_potential_energy()
        sim.computation.cache["total_potential"] = None

def profile_iterallatoms():
    sim = make_montecarlo(num_basic_copies=1, temp=0.1)
    for i in range(1000):
        sim.computation.iter_all_atoms()

def test_burn():
    sim = make_montecarlo(num_basic_copies=1, temp=0.1)
    sim.name = "test_burn"
    sim.deltat = 0.01
    sim.num_steps = 100 * 5
    sim.track_quantity(sim.computation.total_potential_energy, name="total_energy")
    sim.track_quantity(sim.computation.percentage_accepts, name="accepts")
    sim.computation.burn = 600
    sim.computation.prepare() # perform the burn
    sim.run()

def prob3_heatcap():
    sim = make_montecarlo(num_basic_copies=2, temp=0.1)
    sim.name = "prob3_heatcap"
    sim.num_steps = 1000 * 20
    sim.should_write = True
    sim.should_plot = False
    sim.track_quantity(sim.computation.total_potential_energy, name="total_energy")
    sim.track_quantity(sim.computation.percentage_accepts, name="accepts")
    sim.computation.burn = 4000
    sim.computation.delta_scale = 0.08
    sim.computation.prepare() # perform the burn
    sim.run()

def prob4_anneal():
    sim = make_montecarlo(num_basic_copies=2)
    sim.name = "prob4_annealing"
    sim.num_steps = 1000 * 20
    sim.should_write = True
    sim.should_plot = False
    sim.track_quantity(sim.computation.total_potential_energy, name="total_energy")
    sim.track_quantity(sim.computation.percentage_accepts, name="accepts")
    sim.computation.store_initial_positions()
    sim.track_quantity(sim.computation.mean_squared_displacement, name="deltar_squared")
    sim.computation.computationalCell.a *= 1.1 # increase lattice vector by !0%
    sim.computation.burn = 4000
    sim.computation.delta_scale = 0.08
    sim.computation.annealing_schedule = sim.computation.AnnealingSchedule(start=2, end=0, num_steps=2000)

    sim.computation.prepare() # perform the burn
    sim.run()

def profile_nanoparticle():
    sim = make_nanoparticle_montecarlo()
    sim.should_write = False
    sim.should_plot = False
    sim.num_steps = 1000
    sim.run()

if __name__ == "__main__":
    # cProfile.run('test_montecarlo()', sort='cumtime')
    # cProfile.run('test_total_potential()', sort='cumtime')
    # cProfile.run('profile_iterallatoms()', sort='cumtime')
    # prob1()
    
    # cProfile.run('test_md()', sort='cumtime')
    cProfile.run('profile_nanoparticle()', sort='cumtime')


    # test_md()
    # test_storage()
    # test_loading()
    # prob1()
    # prob1_display()
    # cProfile.run('prob1()', sort='time')
    # test_montecarlo()
    # test_burn()
    # prob3_heatcap()
    # prob4_anneal()

