from mesa.batchrunner import BatchRunner
from model import InfectionModel
import simulation_parameters as params


fixed_params = {
    "grid_size": (params.params['grid_width'], params.params['grid_height']),
    "initial_infected_chance": params.params['initial_infected_chance']
}

variable_params = {
    "num_agents": [params.params['num_agents']]
}


def static_run():
    batch_run = BatchRunner(InfectionModel, fixed_parameters=fixed_params,
                            variable_parameters=variable_params, model_reporters={
                                "datacollector": lambda m: m.datacollector
                            }, max_steps=params.params['max_iterations'])
    batch_run.run_all()
    batch_run.get_model_vars_dataframe()\
        .datacollector[0].get_model_vars_dataframe().to_csv('run_data.csv')
