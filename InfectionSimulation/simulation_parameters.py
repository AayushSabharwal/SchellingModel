infection_radius = 3    # how far away from an individual infection can spread
infection_chance = .99  # the base probability for infection to spread
infection_duration = 5  # how long the infection lasts
recovery_chance = 0.8   # the chance with which an individual recovers after infection

grid_size = (20, 20)    # size of the GridXY
num_agents = 150        # number of agents


# value sanity checks
assert num_agents <= grid_size[0] * grid_size[1]
assert infection_radius < min(grid_size[0], grid_size[1])
assert 0. < infection_chance < 1.
assert infection_duration > 0
