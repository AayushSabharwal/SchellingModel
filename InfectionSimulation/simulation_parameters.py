from scipy.stats import erlang
import numpy as np

params = {
    'infection_radius': 2,    # how far away from an individual infection can spread

    'external_infection_chance': 0.01,    # probability that a random susceptible agent will become
    # infected. This models infection coming from outside
    # recovery probability is modeled as an erlang distribution
    'infection_duration_shape': 33,
    'infection_duration_scale': 18.75,
    'mortality_rate': 0.014,  # fraction of agents that contract the disease that die

    # does this disease give immunity on recovery
    'has_recovery_immunity': True,
    # recovery immunity duration is modeled as an erlang distribution
    'recovered_duration_shape': 90,
    'recovered_duration_scale': 80 / 3,

    'vaccination_start': -1,  # how long (days) it takes for a vaccine, -1 for no vaccine
    'newborn_vaccination_rate': 0.7,  # what fraction of newborns are vaccinated each iterations
    'general_vaccination_rate': 0.3,  # what fractions of the general susceptible populace gets vaccinated
    # each iteration

    'mean_distance_per_hour': 4,  # average distance moved by an agent in an hour
    'sd_distance_per_hour': 1,    # standard deviation in distance moved per hour

    'population_birth_rate': 0.0164,  # number of births per day as fraction of currently alive people
    'population_death_rate': 0.0036,  # number of deaths per day as fraction of currently alive people

    'grid_width': 50,    # size of the GridXY
    'grid_height': 50,
    'num_agents': 100,       # number of agents
    'initial_infected_chance': 0.02,   # initial fraction of people infected

    'show_grid': True,  # whether to show the grid during dynamic visualization
    'data_collection_frequency': 1,   # integer, at what interval to collect data
    'max_iterations': 10000,
}


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
    return np.random.normal(params['mean_distance_per_hour'], params['sd_distance_per_hour'])


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
    return erlang.cdf(i, params['infection_duration_shape'], scale=params['infection_duration_scale'])


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
    return erlang.cdf(i, params['recovered_duration_shape'], scale=params['recovered_duration_scale'])


# value sanity checks
def sanity_check():
    # type checking
    assert isinstance(params['infection_radius'], float)
    assert isinstance(params['external_infection_chance'], float)
    assert isinstance(params['infection_duration_shape'], float)
    assert isinstance(params['infection_duration_scale'], float)
    assert isinstance(params['mortality_rate'], float)
    assert isinstance(params['has_recovery_immunity'], bool)
    assert isinstance(params['recovered_duration_shape'], float)
    assert isinstance(params['recovered_duration_scale'], float)
    assert isinstance(params['vaccination_start'], int)
    assert isinstance(params['newborn_vaccination_rate'], float)
    assert isinstance(params['general_vaccination_rate'], float)
    assert isinstance(params['mean_distance_per_hour'], float)
    assert isinstance(params['sd_distance_per_hour'], float)
    assert isinstance(params['population_birth_rate'], float)
    assert isinstance(params['population_death_rate'], float)
    assert isinstance(params['grid_width'], int)
    assert isinstance(params['grid_height'], int)
    assert isinstance(params['num_agents'], int)
    assert isinstance(params['initial_infected_chance'], float)
    assert isinstance(params['show_grid'], bool)
    assert isinstance(params['data_collection_frequency'], int)
    assert isinstance(params['max_iterations'], int)
    # value checks
    assert 1 <= params['infection_radius'] < min(params['grid_width'], params['grid_height'])
    assert 0 <= params['external_infection_chance'] <= 1
    assert params['infection_duration_shape'] > 0
    assert params['infection_duration_scale'] > 0
    assert 0 <= params['mortality_rate'] <= 1
    assert params['recovered_duration_shape'] > 0
    assert params['recovered_duration_scale'] > 0
    assert params['vaccination_start'] >= -1
    assert 0 <= params['newborn_vaccination_rate'] <= 1
    assert 0 <= params['general_vaccination_rate'] <= 1
    assert params['mean_distance_per_hour'] > 0
    assert params['sd_distance_per_hour'] > 0
    assert 0 <= params['population_birth_rate'] <= 1
    assert 0 <= params['population_death_rate'] <= 1
    assert min(params['grid_width'], params['grid_height']) > 0
    assert params['num_agents'] > 0
    assert 0 < params['initial_infected_chance'] < 1
    assert params['data_collection_frequency'] > 0
    assert params['max_iterations'] > 0
