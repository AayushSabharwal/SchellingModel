import random
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from core_simulation import InfectionModel
from simulation_parameters import grid_size, num_agents
from utility import InfectionState


def agent_portrayal(agent):
    """
    Function required for visualization that returns visual representation of an agent
    """
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}

    if agent.state == InfectionState.INF:   # a shade of green for infected
        portrayal["Color"] = "#%02x%02x%02x" % (0, int(255 * random.uniform(0.5, 1)), 0)
    elif agent.state == InfectionState.SUS:  # red for susceptible
        portrayal["Color"] = "#%02x%02x%02x" % (int(255 * random.uniform(0.5, 1)), 0, 0)
    else:                                   # blue for recovered
        portrayal["Color"] = "#%02x%02x%02x" % (0, 0, int(255 * random.uniform(0.5, 1)))
    return portrayal


# visual grid on which agents move
grid = CanvasGrid(agent_portrayal, grid_size[0], grid_size[1], 500, 500)
# chart that plots the number of agents in each state with time
chart = ChartModule([{"Label": "infected", "Color": "green"},
                     {"Label": "recovered", "Color": "blue"},
                     {"Label": "susceptible", "Color": "red"},
                     {"Label": "dead", "Color": "grey"}])

# just mesa stuff
server = ModularServer(InfectionModel, [grid, chart], "Infection Model",
                       {
                       "num_agents": num_agents,
                       "grid_size": grid_size,
                       "initial_infected_chance": 0.05
                       })
server.port = 8521
server.launch()
