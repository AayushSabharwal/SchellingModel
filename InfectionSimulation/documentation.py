documentation = {
    'infection_radius': '''
    How far away from an individual (in metres) infection can spread.
    Must be an integer
    ''',

    'external_infection_chance': '''
    Probability that a random susceptible agent will become infected in any iteration (hour).
    This models infection coming in from outside.
    Must be a float
    ''',

    'infection_duration_shape': '''
    Duration of infection is modeled as an Erlang distribution. This represents the shape parameter.
    Must be a float
    ''',

    'infection_duration_scale': '''
    Duration of infection is modeled as an Erlang distribution. This represents the scale parameter.
    This should be scaled in terms of hours, so if calculated as days, multiply by 24.
    Must be a float.
    ''',

    'mortality_rate': '''
    Fraction of agents that contract the disease that die.
    Must be a float.
    ''',

    'has_recovery_immunity': '''
    Does this disease have an immunity period after recovery?
    ''',

    'recovered_duration_shape': '''
    Recovery duration is modeled as an Erlang distribution. This represents the shape parameter.
    Must be a float.
    ''',

    'recovered_duration_scale': '''
    Recovery duration is modeled as an Erlang distrubtion. This represents the scale parameter.
    This should be scaled in terms of hours, so if calculated as days, multiply by 24.
    Must be a float.
    ''',

    'vaccination_start': '''
    How many hours after start of simulation does a vaccine get developed. Specify -1 for no vaccine.
    Must be an integer.
    ''',

    'newborn_vaccination_rate': '''
    What fraction of newborn agents are vaccinated.
    Must be a float.

    ''',
    'general_vaccination_rate': '''
    What fraction of the general susceptible population gets vaccinated every iteration (hour).
    Must be a float.
    ''',

    'mean_distance_per_hour': '''
    Distance moved per hour is modeled as a Normal distribution. This is the mean value.
    Must be a float.
    ''',

    'sd_distance_per_hour': '''
    Distance moved per hour is modeled as a Normal distribution. This is the standard deviation.
    Must be a float.
    ''',

    'population_birth_rate': '''
    Birth rate of the population, specified as number of births per year as a fraction of currently alive people.
    Must be a float.

    ''',
    'population_death_rate': '''
    Death rate of the population, specified as number of deaths per year as a fraction of currently alive people.
    Must be a float.
    ''',

    'grid_width': '''
    Width of the grid on which simulation occurs. Specified in meters.
    Must be an integer.
    ''',

    'grid_height': '''
    Height of the grid on which the simulation occurs. Specified in meters.
    Must be an integer.
    ''',

    'num_agents': '''
    Total number of agents in the simulation.
    Must be an integer.
    ''',

    'initial_infected_chance': '''
    Initial fraction of infected agents.
    Must be a float.
    ''',

    'show_grid': '''
    Specific to Dynamic Visualization. Specifies whether the grid should be shown or not.
    ''',

    'data_collection_frequency': '''
    At what frequency (after how many iterations) should data be collected.
    Note that this does not affect granularity or speed of simulation, only the granularity of data.
    Must be an integer.
    ''',

    'max_iterations': '''
    Specific to Static Visualzation. Specifies the maximum number of iterations the simulation should be run for.
    The simulation automatically ends when there are no infected agents.
    Must be an integer.
    ''',
}
