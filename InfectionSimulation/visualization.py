from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from core_simulation import InfectionModel
from simulation_parameters import grid_size, num_agents, initial_infected_chance
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
                      {"Label": "alive", "Color": "black"}])
chart2 = ChartModule([{"Label": "total_infections", "Color": "green"},
                      {"Label": "total_recoveries", "Color": "blue"},
                      {"Label": "deaths", "Color": "grey"}])
# just mesa stuff
server = ModularServer(InfectionModel, [chart1, chart2], "Infection Model",
                       {
                       "num_agents": num_agents,
                       "grid_size": grid_size,
                       "initial_infected_chance": initial_infected_chance
                       })
server.port = 8521
server.launch()
