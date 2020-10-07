infection_radius = 3    # how far away from an individual infection can spread
infection_chance = .7  # the base probability for infection to spread
infection_duration = 6  # how long the infection lasts
recovery_chance = 0.8   # the chance with which an individual recovers after infection
recovered_duration = 0  # how long agents stay recoevered. -1 for infinitely

population_birth_rate = 0.1  # number of births per iteration as a fraction of currently alive people
population_death_rate = 0.1  # number of deaths per iteration as a fraction of currently alive people

grid_size = (50, 50)    # size of the GridXY
num_agents = 1000        # number of agents


# value sanity checks
assert num_agents <= grid_size[0] * grid_size[1]
assert infection_radius < min(grid_size[0], grid_size[1])
assert 0. < infection_chance <= 1.
assert infection_duration > 0
assert recovered_duration >= -1
assert 0 <= population_birth_rate <= 1
