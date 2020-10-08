from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from type_hints import GridXY
from utility import InfectionState, sqr_euler_distance
import simulation_parameters as params


class InfectionModel(Model):
    """
    Mesa model class that simulates infection spread
    """

    def __init__(self, num_agents: int, grid_size: GridXY, initial_infected_chance: float):
        """
        Parameters
        ----------
        num_agents : int
            Number of agents initially created in simulation
        grid_size : GridXY
            Size of simulation grid
        initial_infected_chance : float
            Initial fraction of people who are infected
        """
        self.num_agents = 0    # total agents to ever exist
        self.statistics = {     # statistics for data collector
            "infected": 0,
            "recovered": 0,
            "susceptible": 0,
            "vaccinated": 0,
            "deaths": 0,
            "alive": 0,
            "total_infections": 0,
            "total_recoveries": 0,
        }

        self.grid = MultiGrid(grid_size[0], grid_size[1], True)  # grid that the agent move on
        self.schedule = SimultaneousActivation(self)    # scheduler for iterations of the simulation
        self.datacollector = DataCollector(model_reporters={    # to collect data for the graph
            "infected": lambda m: m.statistics["infected"],
            "recovered": lambda m: m.statistics["recovered"],
            "susceptible": lambda m: m.statistics["susceptible"],
            "vaccinated": lambda m: m.statistics["vaccinated"],
            "deaths": lambda m: m.statistics["deaths"],
            "alive": lambda m: m.statistics["alive"],
            "total_infections": lambda m: m.statistics["total_infections"],
            "total_recoveries": lambda m: m.statistics["total_recoveries"],
        })

        self.running = True                # required for visualization, tells if simulation is done
        self.dead_agents = []   # when agents die, they are added to this list to be removed
        self.step_count = 0     # number of steps completed, required for vaccination
        self.vaccination_started = False    # has vaccination started?

        # creating agents
        for _ in range(num_agents):
            # initial state of this agent
            initial_state = InfectionState.INF if \
                self.random.uniform(0, 1) < initial_infected_chance else InfectionState.SUS
            # randomise position
            pos = self.random.randrange(self.grid.width), self.random.randrange(self.grid.height)
            self.add_agent(self.create_agent(initial_state), pos)

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

        self.handle_births_and_deaths()  # simulate births and deaths
        self.calculate_statistics()  # calculate statistics for data collector
        self.schedule.step()    # run step for all agents
        self.datacollector.collect(self)    # collect data

        self.step_count += 1
        # if vaccination is enabled and enough time has passed
        if not self.vaccination_started and params.vaccination_start != -1 and \
                self.step_count > params.vaccination_start:
            self.vaccination_started = True  # start vaccination

        for x in self.dead_agents:  # remove dead agents
            self.remove_agent(x)
            self.statistics["deaths"] += 1   # add to death count
        self.dead_agents = []
        self.running = self.check_running()  # is the simulation still running?

    def calculate_statistics(self):
        """
        Calculates statistics each iteration, for more efficient data collection
        """
        # reset all iteration specific parameters
        self.statistics["infected"] = 0
        self.statistics["recovered"] = 0
        self.statistics["susceptible"] = 0
        self.statistics["vaccinated"] = 0
        self.statistics["alive"] = 0

        for agent in self.schedule.agent_buffer():
            self.statistics["alive"] += 1
            if agent.state == InfectionState.INF:
                self.statistics["infected"] += 1
            elif agent.state == InfectionState.SUS:
                self.statistics["susceptible"] += 1
            elif agent.state == InfectionState.REC:
                self.statistics["recovered"] += 1
            elif agent.state == InfectionState.VAC:
                self.statistics["vaccinated"] += 1

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
                # the newborn agent is vaccinated if it has started and with given probability,
                # otherwise it is susceptible
                initial_state = InfectionState.VAC if self.vaccination_started and \
                    self.random.uniform(0, 1) < params.newborn_vaccination_rate \
                    else InfectionState.SUS
                # add agent to list
                agents_to_add.append((self.create_agent(initial_state), agent.pos))

            if self.random.uniform(0, 1) <\
                    params.population_death_rate:
                self.remove_agent(agent)

        # actually add those agents to the simulation
        for agent in agents_to_add:
            self.add_agent(agent[0], agent[1])

    def create_agent(self, initial_state: InfectionState):
        """
        Creates an agent, and returns it

        Parameters
        ----------
        initial_state : InfectionState
            Initial state of this agent
        """
        self.num_agents += 1
        return PersonAgent(self.num_agents - 1, self, initial_state)  # create agent

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

    def __init__(self, u_id: int, model: InfectionModel, initial_state: InfectionState):
        """
        Parameters
        ----------
        u_id : int
            Unique id for the agent, required by mesa
        model : InfectionModel
            Model that created and handles this agent. Must have grid and scheduler (simultaenous)
        initial_state : InfectionState
            Initial state of this agent
        """
        # call base __init__
        super().__init__(u_id, model)
        # current state of this agent. Check utility.py for possible states
        self.state = initial_state
        # how long recovery immunity lasts
        self.recovery_timeout = 0

        # the state the agent will have at the end of this iteration. This is a requirement for
        # simultaneous activation, since each agent first calculates its changes and then
        # applies them
        self.target_state = None

    def infect(self):
        """
        Called when an agent is infected by another agent
        """
        self.target_state = InfectionState.INF
        self.model.statistics["total_infections"] += 1

    def infection_recovery(self):
        """
        Randomly has a probability to become recovered each iteration, based on infection_duration,
        or die, based on mortality_rate
        """
        p = self.random.uniform(0, 1)
        if p < 1. / params.infection_duration:  # if agent recovers
            self.model.statistics["total_recoveries"] += 1
            if params.recovered_duration == 0:  # if there is no immunity stage
                # agents go back to susceptibility
                self.target_state = InfectionState.SUS
            else:   # otherwise, they will go to the recovery state
                self.target_state = InfectionState.REC
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
            # after recovering, agent is now susceptible again
            self.target_state = InfectionState.SUS

    def try_vaccination(self):
        """
        Called on susceptible agents, has a chance for them to get vaccinated
        """
        if self.model.vaccination_started and \
                self.random.uniform(0, 1) < params.general_vaccination_rate:
            self.target_state = InfectionState.VAC

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
        Called every agent step, stages changes to be applied
        """
        self.move()
        if self.state == InfectionState.INF:    # every infected agent...
            self.spread()                       # spreads the infections
            self.infection_recovery()           # and has a chance to recover
        elif params.recovered_duration != -1 and self.state == InfectionState.REC:
            self.recovery_timer()
        elif self.state == InfectionState.SUS:
            self.try_vaccination()

    def advance(self):
        """
        Applies changes staged in step()
        """
        if self.target_state is None:   # return if no changes to be staged
            return
        self.state = self.target_state  # apply state change
        self.target_state = None        # reset
