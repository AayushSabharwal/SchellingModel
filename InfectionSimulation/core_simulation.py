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


def get_num_alive(model):
    return len(list(model.schedule.agent_buffer()))


class InfectionModel(Model):
    """
    Mesa model class that simulates infection spread
    """

    def __init__(self, num_agents: int, grid_size: GridXY, initial_infected_chance: float):
        self.num_agents = 0    # total agents to ever exist
        self.grid = MultiGrid(grid_size[0], grid_size[1], True)  # grid that the agent move on
        self.schedule = SimultaneousActivation(self)    # scheduler for iterations of the simulation
        self.datacollector = DataCollector(model_reporters={    # to collect data for the graph
                                           "infected": get_num_infected,
                                           "recovered": get_num_recovered,
                                           "susceptible": get_num_susceptible,
                                           "dead": get_num_dead,
                                           "alive": get_num_alive
                                           })
        self.running = True                # required for visualization, tells if simulation is done
        self.dead_agents = []   # when agents die, they are added to this list to be removed
        self.death_count = 0

        # creating agents
        for _ in range(num_agents):
            # is this agent infected at random
            infected = self.random.uniform(0, 1) < initial_infected_chance
            # randomise position
            pos = self.random.randrange(self.grid.width), self.random.randrange(self.grid.height)
            self.add_agent(self.create_agent(infected), pos)

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
        # simulate births and deaths
        self.handle_births_and_deaths()
        self.schedule.step()    # run step for all agents
        self.datacollector.collect(self)    # collect data

        for x in self.dead_agents:  # remove dead agents
            self.remove_agent(x)
            self.death_count += 1   # add to death count
        self.dead_agents = []
        self.running = self.check_running()  # is the simulation still running?

    def handle_births_and_deaths(self):
        """
        Simulates births and deaths in a population
        """
        agents_to_add = []  # all the agents created
        for agent in self.schedule.agent_buffer():
            # make sure to not iterate over just created agents
            if agent in agents_to_add:
                continue

            if self.random.uniform(0, 1) < params.population_birth_rate:
                agents_to_add.append((self.create_agent(False), agent.pos))  # add agent to list

            if self.random.uniform(0, 1) <\
                    params.population_death_rate:
                self.remove_agent(agent)

        # actually add those agents to the simulation
        for agent in agents_to_add:
            self.add_agent(agent[0], agent[1])

    def create_agent(self, infected: bool):
        """
        Creates an agent, and returns it
        """
        self.num_agents += 1
        return PersonAgent(self.num_agents - 1, self, infected)  # create agent

    def add_agent(self, agent: Agent, pos: GridXY):
        """
        Adds an agent to the simulation
        """
        self.schedule.add(agent)    # add to scheduler
        # assign position
        self.grid.place_agent(agent, pos)

    def remove_agent(self, agent: Agent):
        """
        Removes an agent from the simulation
        """
        self.grid.remove_agent(agent)
        self.schedule.remove(agent)


class PersonAgent(Agent):
    """
    Agent class
    """

    def __init__(self, u_id: int, model: InfectionModel, is_infected: bool):
        super().__init__(u_id, model)
        # current state of this agent. Check utility.py for possible states
        self.state = InfectionState.INF if is_infected else InfectionState.SUS
        # how long recovery immunity lasts
        self.recovery_timeout = 0

    def infect(self):
        """
        Called when an agent is infected by another agent
        """
        self.state = InfectionState.INF

    def infection_recovery(self):
        """
        Randomly has a probability to become recovered each iteration, based on infection_duration,
        or die, based on mortality_rate
        """
        p = self.random.uniform(0, 1)
        if p < 1. / params.infection_duration:  # if agent recovers
            self.state = InfectionState.REC
            self.recovery_timeout = params.recovered_duration
        elif p < 1. / params.infection_duration + params.mortality_rate:  # if agent dies
            self.model.dead_agents.append(self)

    def recovery_timer(self):
        """
        Decrements the recovery timer. Only called if the recovered agents can become susceptible
        after some time
        """
        self.recovery_timeout -= 1
        if self.recovery_timeout <= 0:
            self.recovery_timeout = 0
            self.state = InfectionState.SUS  # after recovering, agent is now susceptible again

    def spread(self):
        """
        Called on infected agents, to spread infection
        """
        # iterate through all agents in 3 unit radius neighbourhood
        for agent in self.model.grid.iter_cell_list_contents(self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=True, radius=params.infection_radius)):
            # we can only infect susceptible individuals
            if agent.state == InfectionState.SUS:
                # the chance for a susceptible individual to get infected is inversely proportional
                # to the square of the euler distance between the two agents
                if self.random.uniform(0, 1) < params.infection_chance /\
                        max(sqr_euler_distance(self.pos, agent.pos), 1):
                    agent.infect()

    def move(self):
        """
        Moves agent randomly in Von Neumann neighbourhood
        """
        neighbours = self.model.grid.get_neighborhood(self.pos, moore=False)
        self.model.grid.move_agent(self, self.random.choice(neighbours))

    def step(self):
        """
        Called every agent step
        """
        self.move()
        if self.state == InfectionState.INF:    # every infected agent...
            self.spread()                       # spreads the infections
            self.infection_recovery()           # and has a chance to recover

        # for recovered agents. This is not in an elif to also execute on the step where
        # infection_recovery makes this agent recovered
        if params.recovered_duration != -1 and self.state == InfectionState.REC:
            self.recovery_timer()
