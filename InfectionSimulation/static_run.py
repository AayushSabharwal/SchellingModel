try:
    from model import InfectionModel
except ImportError:
    from InfectionSimulation.model import InfectionModel


def static_run(params: dict):
    model = InfectionModel(params)
    for i in range(params['max_iterations']):
        model.step()
        if not model.running:
            break
    model.dataCollector.get_model_vars_dataframe().to_csv('run_data.csv', index=False)
