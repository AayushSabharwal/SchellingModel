infection_radius = 3
infection_chance = .99
infection_duration = 5
recovery_chance = 0.8

grid_size = (20, 20)
num_agents = 150

assert num_agents <= grid_size[0] * grid_size[1]
assert infection_radius < min(grid_size[0], grid_size[1])
assert 0. < infection_chance < 1.
assert infection_duration > 0
