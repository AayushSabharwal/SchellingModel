from typing import Tuple
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
try:
    from agent import PersonAgent
    from utility import InfectionState
except ImportError:
    from InfectionSimulation.agent import PersonAgent
    from InfectionSimulation.utility import InfectionState


# noinspection PyMissingConstructor
class InfectionModel(Model):
    """
    Mesa model class that simulates infection spread
    """

    def __init__(self, params: dict):
        """
        Parameters
        ----------
        params: dict
            Simulation parameters
        """
        self.current_id = 0     # inherited variable, for id generation
        self.params = params    # parameters
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

        self.grid = MultiGrid(self.params['grid_width'], self.params['grid_height'], True)  # grid that agents move on
        self.schedule = SimultaneousActivation(self)    # scheduler for iterations of the simulation
        self.dataCollector = DataCollector(model_reporters={    # to collect data for the graph
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
        for _ in range(self.params['num_agents']):
            # initial state of this agent
            initial_state = InfectionState.INF if \
                self.random.uniform(0, 1) < self.params['initial_infected_chance'] else InfectionState.SUS

            # by default, this won't add to total_infections which leads to incorrect results
            if initial_state == InfectionState.INF:
                self.statistics["total_infections"] += 1
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
        # just to show the progress while running in console
        if self.step_count % 100 == 0:
            print(self.step_count)
        self.per_agent_actions()  # simulate actions to be taken globally on all agents
        self.schedule.step()    # run step for all agents

        # collect data at a particular frequency
        if self.step_count % self.params['data_collection_frequency'] == 0:
            self.calculate_statistics()  # calculate statistics for data collector
            self.dataCollector.collect(self)    # collect data

        self.step_count += 1
        # if vaccination is enabled and enough time has passed
        if not self.vaccination_started and self.params['vaccination_start'] != -1 and \
                self.step_count > self.params['vaccination_start']:
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

    def per_agent_actions(self):
        """
        Simulates actions to be taken on a global scale per agent
        """
        # this should only occur once a day
        if self.step_count % 24 != 0:
            return
        for agent in self.schedule.agent_buffer():
            if self.random.uniform(0, 1) < self.params['external_infection_chance']:
                agent.state = InfectionState.INF
                self.statistics["total_infections"] += 1

    def create_agent(self, initial_state: InfectionState) -> PersonAgent:
        """
        Creates an agent, and returns it

        Parameters
        ----------
        initial_state : InfectionState
            Initial infection state of this agent

        Returns
        -------
        PersonAgent
            The agent created
        """
        return PersonAgent(self.next_id(), self, initial_state)

    def add_agent(self, agent: Agent, pos: Tuple[int, int]):
        """
        Adds an agent to the simulation

        Parameters
        ----------
        agent : agent
            The agent to be added

        pos : Tuple[int, int]
            The position where this agent should be on the grid
        """
        # add to scheduler
        self.schedule.add(agent)
        # assign position
        self.grid.place_agent(agent, pos)

    def remove_agent(self, agent: Agent):
        """
        Removes an agent from the simulation

        Parameters
        ----------
        agent : Agent
            The agent to be removed from the simulation
        """
        self.grid.remove_agent(agent)
        self.schedule.remove(agent)
