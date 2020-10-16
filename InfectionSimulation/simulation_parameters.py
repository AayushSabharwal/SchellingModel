from scipy.stats import erlang
import numpy as np


infection_radius = 2    # how far away from an individual infection can spread

external_infection_chance = 0.01    # probability that a random susceptible agent will become
# infected. This models infection coming from outside
# recovery probability is modeled as an erlang distribution
infection_duration_shape = 33
infection_duration_scale = 18.75
mortality_rate = 0.014   # fraction of agents that contract the disease that die

# does this disease give immunity on recovery
has_recovery_immunity = True
# recovery immunity duration is modeled as an erlang distribution
recovered_duration_shape = 90
recovered_duration_scale = 80 / 3

vaccination_start = -1  # how long (days) it takes for a vaccine, -1 for no vaccine
newborn_vaccination_rate = 0.7  # what fraction of newborns are vaccinated each iterations
general_vaccination_rate = 0.3  # what fractions of the general susceptible populace gets vaccinated
# each iteration

mean_distance_per_hour = 4  # average distance moved by an agent in an hour
sd_distance_per_hour = 1    # standard deviation in distance moved per hour

population_birth_rate = 0.0164  # number of births per day as fraction of currently alive people
population_death_rate = 0.0036  # number of deaths per day as fraction of currently alive people


def infection_chance(dist: float):
    """
    Calculates infection chance for being at dist metres from an infected individual

    Parameters
    ----------
    dist : float
        Distance between individuals

    Returns
    -------
    float
        Probability that infection will occur
    """
    distr = [0.13, 0.06, 0.03]
    mean = distr[min(round(dist), len(distr) - 1)]
    return np.random.normal(mean, mean / 10)


def movement_distance():
    """
    Calculates distance to move for an agent in an iterations

    Returns
    -------
    int
        Distance to move
    """
    return np.random.normal(mean_distance_per_hour, sd_distance_per_hour)


def infection_end_chance(i: int):
    """
    Calculates probability that an individual's infection will end

    Parameters
    ----------
    i : int
        The number of iterations since infection

    Returns
    -------
    float
        Probability that individual will recover
    """
    return erlang.cdf(i, infection_duration_shape, scale=infection_duration_scale)


def recovered_end_chance(i: int):
    """
    Calculates probability that an individual will lose recovery immunity and become susceptible
    again

    Parameters
    ----------
    i : int
        The number of iterations since recovery

    Returns
    -------
    float
        Probability that recovery immunity will end
    """
    return erlang.cdf(i, recovered_duration_shape, scale=recovered_duration_scale)


grid_size = (50, 50)    # size of the GridXY
num_agents = 100        # number of agents
initial_infected_chance = 0.02   # initial fraction of people infected

show_grid = True   # whether to show the grid during dynamic visualization
data_collection_frequency = 1   # integer, at what interval to collect data
max_iterations = 10000


# value sanity checks
assert min(grid_size) >= 10
assert 1 <= num_agents <= grid_size[0] * grid_size[1]
assert 1 <= infection_radius < min(grid_size)
assert 0 <= external_infection_chance <= 1
assert 0 <= mortality_rate <= 1
assert 0 <= population_birth_rate <= 1
assert vaccination_start >= -1
assert 0 <= newborn_vaccination_rate <= 1
assert 0 <= newborn_vaccination_rate <= 1
assert data_collection_frequency >= 1
assert max_iterations >= 1
