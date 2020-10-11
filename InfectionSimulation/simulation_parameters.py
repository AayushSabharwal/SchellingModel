infection_radius = 2    # how far away from an individual infection can spread

external_infection_chance = 0.01    # probability that a random susceptible agent will become
# infected. This models infection coming from outside
infection_chance = 0.5  # the base probability for infection to spread
recovery_probability = 1 / 7  # probability that an infected agent recovers at any given day
# this can be interpreted as 1/D, where D is average duration of infection (in days)
mortality_rate = 0.00044   # probability that an infected agent will die in any day

recovered_duration = 90  # how long agents stay recovered. -1 for infinitely

vaccination_start = -1  # how long (days) it takes for a vaccine, -1 for no vaccine
newborn_vaccination_rate = 0.7  # what fraction of newborns are vaccinated each iterations
general_vaccination_rate = 0.3  # what fractions of the general susceptible populace gets vaccinated
# each iteration

population_birth_rate = 0.0164  # number of births per day as fraction of currently alive people
population_death_rate = 0.0036  # number of deaths per day as fraction of currently alive people

grid_size = (1000, 1000)    # size of the GridXY
num_agents = 7500        # number of agents
initial_infected_chance = 0.02   # initial fraction of people infected

show_grid = False   # whether to show the grid during dynamic visualization
data_collection_frequency = 1   # integer, at what interval to collect data

# value sanity checks
assert num_agents <= grid_size[0] * grid_size[1]
assert infection_radius < min(grid_size[0], grid_size[1])
assert 0 < infection_chance <= 1
assert 0 <= recovery_probability <= 1
assert 0 <= mortality_rate <= 1
assert recovery_probability + mortality_rate <= 1
assert recovered_duration >= -1
assert 0 <= population_birth_rate <= 1
assert vaccination_start >= -1
assert 0 <= newborn_vaccination_rate <= 1
assert 0 <= newborn_vaccination_rate <= 1
