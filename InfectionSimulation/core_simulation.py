from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from type_hints import GridXY
from utility import InfectionState, sqr_euler_distance
import simulation_parameters as params


def get_num_infected(model):
    return len([a for a in model.schedule.agent_buffer() if a.state == InfectionState.INF])


def get_num_recovered(model):
    return len([a for a in model.schedule.agent_buffer() if a.state == InfectionState.REC])


def get_num_susceptible(model):
    return len([a for a in model.schedule.agent_buffer() if a.state == InfectionState.SUS])


def get_num_dead(model):
    return model.death_count


class InfectionModel(Model):
    def __init__(self, num_agents: int, grid_size: GridXY, initial_infected_chance: float):
        self.num_agents = num_agents
        self.grid = MultiGrid(grid_size[0], grid_size[1], True)
        self.schedule = SimultaneousActivation(self)
        self.datacollector = DataCollector(model_reporters={
                                           "infected": get_num_infected,
                                           "recovered": get_num_recovered,
                                           "susceptible": get_num_susceptible,
                                           "dead": get_num_dead
                                           })
        self.running = True
        self.dead_agents = []
        self.death_count = 0

        for i in range(self.num_agents):
            infected = self.random.uniform(0, 1) < initial_infected_chance
            agent = PersonAgent(i, self, infected)
            self.schedule.add(agent)

            pos = self.random.randrange(self.grid.width), self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, pos)

    def check_running(self):
        for agent in self.schedule.agent_buffer():
            if agent.state == InfectionState.INF:
                return True
        return False

    def step(self):
        self.running = self.check_running()
        self.datacollector.collect(self)
        self.schedule.step()
        for x in self.dead_agents:
            self.grid.remove_agent(x)
            self.schedule.remove(x)
            self.death_count += 1
        self.dead_agents = []


class PersonAgent(Agent):
    def __init__(self, u_id: int, model: InfectionModel, is_infected: bool):
        super().__init__(u_id, model)
        self.state = InfectionState.INF if is_infected else InfectionState.SUS
        self.infection_timeout = params.infection_duration if is_infected else 0

    def infect(self):
        self.infection_timeout = params.infection_duration
        self.state = InfectionState.INF

    def infection_timer(self):
        self.infection_timeout -= 1
        if self.infection_timeout <= 0:
            self.infection_timeout = 0
            if self.random.uniform(0, 1) < params.recovery_chance:
                self.state = InfectionState.REC
            else:
                self.model.dead_agents.append(self)

    def spread(self):
        for agent in self.model.grid.iter_cell_list_contents(self.model.grid.get_neighborhood(
                self.pos, True, radius=params.infection_radius)):
            if agent.state == InfectionState.INF or agent.state == InfectionState.REC:
                continue
            if self.random.uniform(0, 1) < params.infection_chance /\
                    sqr_euler_distance(self.pos, agent.pos):
                agent.infect()

    def move(self):
        neighbours = self.model.grid.get_neighborhood(self.pos, moore=False)
        self.model.grid.move_agent(self, self.random.choice(neighbours))

    def step(self):
        self.move()
        if self.state == InfectionState.INF:
            self.spread()
            self.infection_timer()
