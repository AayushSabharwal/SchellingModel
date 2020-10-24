"""
To show a live updating plot of statistics and optionally a grid animation
"""
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
try:
    from model import InfectionModel
    import simulation_parameters as params
    from utility import InfectionState
except ImportError:
    from InfectionSimulation.model import InfectionModel
    from InfectionSimulation.utility import InfectionState


def agent_portrayal(agent):
    """
    Function required for visualization that returns visual representation of an agent
    """
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}

    if agent.state == InfectionState.INF:   # a shade of green for infected
        portrayal["Color"] = "green"
    elif agent.state == InfectionState.SUS:  # red for susceptible
        portrayal["Color"] = "red"
    elif agent.state == InfectionState.REC:  # blue for recovered
        portrayal["Color"] = "blue"
    else:                                   # yellow for vaccinated
        portrayal["Color"] = "yellow"
    return portrayal


# chart that plots the number of agents in each state with time
chart1 = ChartModule([{"Label": "infected", "Color": "green"},
                      {"Label": "recovered", "Color": "blue"},
                      {"Label": "susceptible", "Color": "red"},
                      {"Label": "vaccinated", "Color": "yellow"},
                      {"Label": "alive", "Color": "black"}], data_collector_name='dataCollector')
# cumulative statistics chart
chart2 = ChartModule([{"Label": "total_infections", "Color": "green"},
                      {"Label": "total_recoveries", "Color": "blue"},
                      {"Label": "deaths", "Color": "grey"}], data_collector_name='dataCollector')
# just mesa stuff
visualization_elements = [chart1, chart2]


def dynamic_run(params: dict):
    if params['show_grid']:
        # visual grid on which agents move
        grid = CanvasGrid(agent_portrayal, params['grid_width'], params['grid_height'],
                          500, 500)
        visualization_elements.insert(0, grid)

    server = ModularServer(InfectionModel, visualization_elements, "Infection Model", {"params": params})
    server.port = 8521
    server.launch()
