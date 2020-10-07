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
    """
    Mesa model class that simulates infection spread
    """

    def __init__(self, num_agents: int, grid_size: GridXY, initial_infected_chance: float):
        self.num_agents = num_agents    # self explanatory
        self.grid = MultiGrid(grid_size[0], grid_size[1], True)  # grid that the agent move on
        self.schedule = SimultaneousActivation(self)    # scheduler for iterations of the simulation
        self.datacollector = DataCollector(model_reporters={    # to collect data for the graph
                                           "infected": get_num_infected,
                                           "recovered": get_num_recovered,
                                           "susceptible": get_num_susceptible,
                                           "dead": get_num_dead
                                           })
        self.running = True                # required for visualization, tells if simulation is done
        self.dead_agents = []   # when agents die, they are added to this list to be removed
        self.death_count = 0

        # creating agents
        for i in range(self.num_agents):
            # is this agent infected at random
            infected = self.random.uniform(0, 1) < initial_infected_chance
            agent = PersonAgent(i, self, infected)  # create agent
            self.schedule.add(agent)    # add to scheduler
            # randomise and assign position
            pos = self.random.randrange(self.grid.width), self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, pos)

    def check_running(self):
        """
        Checks and returns if the simulation is still running (there are infected people)
        """
        for agent in self.schedule.agent_buffer():
            if agent.state == InfectionState.INF:
                return True
        return False

    def step(self):
        """
        Called every step
        """
        self.running = self.check_running()  # is the simulation still running?
        self.datacollector.collect(self)    # collect data
        self.schedule.step()    # run step for all agents
        for x in self.dead_agents:  # remove dead agents
            self.grid.remove_agent(x)
            self.schedule.remove(x)
            self.death_count += 1   # add to death count
        self.dead_agents = []


class PersonAgent(Agent):
    """
    Agent class
    """

    def __init__(self, u_id: int, model: InfectionModel, is_infected: bool):
        super().__init__(u_id, model)
        # current state of this agent. Check utility.py for possible states
        self.state = InfectionState.INF if is_infected else InfectionState.SUS
        # how long the infection takes to go away
        self.infection_timeout = params.infection_duration if is_infected else 0
        self.recovery_timeout = 0

    def infect(self):
        """
        Called when an agent is infected by another agent
        """
        self.infection_timeout = params.infection_duration
        self.state = InfectionState.INF

    def infection_timer(self):
        """
        Decrements the infection timer. Once 0, the agent may recover or die (randomly)
        """
        self.infection_timeout -= 1
        if self.infection_timeout <= 0:  # if the infection is over
            self.infection_timeout = 0
            if self.random.uniform(0, 1) < params.recovery_chance:  # is this agent recovered...
                self.state = InfectionState.REC
                self.recovery_timeout = params.recovered_duration
            else:
                self.model.dead_agents.append(self)  # ...or dead?

    def recovery_timer(self):
        """
        Decrements the recovery timer. Only called if the recovered agents can become susceptible
        after some time
        """
        self.recovery_timeout -= 1
        if self.recovery_timeout <= 0:
            self.recovery_timeout = 0
            self.state = InfectionState.SUS

    def spread(self):
        """
        Called on infected agents, to spread infection
        """
        # iterate through all agents in 3 unit radius neighbourhood
        for agent in self.model.grid.iter_cell_list_contents(self.model.grid.get_neighborhood(
                self.pos, moore=True, radius=params.infection_radius)):
            # we can't infect those already infected or those recovered (immune)
            if agent.state == InfectionState.INF or agent.state == InfectionState.REC:
                continue
            # the chance for a susceptible individual to get infected is inversely proportional
            # to the square of the euler distance between the two agents
            if self.random.uniform(0, 1) < params.infection_chance /\
                    sqr_euler_distance(self.pos, agent.pos):
                agent.infect()

    def move(self):
        """
        Moves agent randomly in Von Neumann neighbourhood
        """
        neighbours = self.model.grid.get_neighborhood(self.pos, moore=False)
        self.model.grid.move_agent(self, self.random.choice(neighbours))

    def step(self):
        self.move()
        if self.state == InfectionState.INF:
            self.spread()
            self.infection_timer()
        elif params.recovered_duration != -1 and self.state == InfectionState.REC:
            self.recovery_timer()
