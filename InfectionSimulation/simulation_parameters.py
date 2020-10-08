infection_radius = 3    # how far away from an individual infection can spread

infection_chance = 0.9  # the base probability for infection to spread
infection_duration = 6  # how long the infection lasts, interpreted as inverse of probability
# of recovering at any given day
mortality_rate = 0.2   # probability that an infected agent will die in an iteration

recovered_duration = 1  # how long agents stay recovered. -1 for infinitely

vaccination_start = 20  # how long it takes for a vaccine to come into effect, -1 for no vaccine
newborn_vaccination_rate = 0.7  # what fraction of newborns are vaccinated each iterations
general_vaccination_rate = 0.3  # what fractions of the general susceptible populace gets vaccinated
# each iteration

population_birth_rate = 0.1  # number of births per iteration as fraction of currently alive people
population_death_rate = 0.1  # number of deaths per iteration as fraction of currently alive people

grid_size = (50, 50)    # size of the GridXY
num_agents = 1000        # number of agents


# value sanity checks
assert num_agents <= grid_size[0] * grid_size[1]
assert infection_radius < min(grid_size[0], grid_size[1])
assert 0. < infection_chance <= 1.
assert infection_duration > 0
assert recovered_duration >= -1
assert 0 <= population_birth_rate <= 1
assert vaccination_start >= -1
assert 0 <= newborn_vaccination_rate <= 1
assert 0 <= newborn_vaccination_rate <= 1
