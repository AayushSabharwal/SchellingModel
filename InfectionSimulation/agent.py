from math import sin, cos, pi
from mesa import Agent, Model
try:
    import simulation_parameters as params
except ImportError:
    from . import simulation_parameters as params
try:
    from utility import InfectionState, toroidal_distance
except ImportError:
    from .utility import InfectionState, toroidal_distance


class PersonAgent(Agent):
    """
    Agent class
    """

    def __init__(self, u_id: int, model: Model, initial_state: InfectionState):
        """
        Parameters
        ----------
        u_id : int
            Unique id for the agent, required by mesa
        model : InfectionModel
            Model that created and handles this agent. Must have grid and scheduler (simultaenous)
        initial_state : InfectionState
            Initial infection state of this agent
        """
        # call base __init__
        super().__init__(u_id, model)
        # current state of this agent. Check utility.py for possible states
        self.state = initial_state
        # how long the agent is infected
        self.infection_duration = 0
        # how long the agent has been recovered
        self.recovered_duration = 0
        # the state the agent will have at the end of this iteration. This is a requirement for
        # simultaneous activation, since each agent first calculates its changes and then
        # applies them
        self.target_state = None
        # toggled in self.simulate_birth, and applied in self.advance
        self.give_birth = False
        # will this agent die this step?
        self.die = False

    def simulate_birth(self):
        """
        Simulates individuals giving birth. This occurs with probability as specified in params
        """
        # divided by 8760 to convert yearly fraction to hourly
        if self.random.uniform(0, 1) < params.params['population_birth_rate'] / 8760:
            self.give_birth = True

    def simulate_death(self):
        """
        Simulates death, occurs with probbility as specified in params
        """
        # divided by 8760 to convert yearly fraction to hourly
        if self.random.uniform(0, 1) < params.params['population_death_rate'] / 8760:
            self.die = True

    def infect(self):
        """
        Called when an agent is infected by another agent
        """
        self.target_state = InfectionState.INF
        self.model.statistics["total_infections"] += 1
        self.infection_duration = 0

    def infection_period(self):
        """
        Randomly has a probability to become recovered each iteration, based on infection_duration,
        or die, based on mortality_rate
        """
        if self.random.uniform(0, 1) < params.infection_end_chance(self.infection_duration):
            if self.random.uniform(0, 1) < params.params['mortality_rate']:
                self.model.dead_agents.append(self)
            else:
                self.model.statistics["total_recoveries"] += 1
                if params.params['has_recovery_immunity']:  # if there is no immunity stage
                    # agents go back to susceptibility
                    self.target_state = InfectionState.SUS
                else:   # otherwise, they will go to the recovery state
                    self.target_state = InfectionState.REC
                    self.recovered_duration = 0

    def recovery_timer(self):
        """
        Simulates recovery immunity ending
        """
        # recovery chance is inversely proportional to average recovered duration
        if self.random.uniform(0, 1) < params.recovered_end_chance(self.recovered_duration):
            # after recovering, agent is now susceptible again
            self.target_state = InfectionState.SUS

    def try_vaccination(self):
        """
        Called on susceptible agents, has a chance for them to get vaccinated
        """
        if self.model.vaccination_started and \
                self.random.uniform(0, 1) < params.params['general_vaccination_rate']:
            self.target_state = InfectionState.VAC

    def spread(self):
        """
        Called on infected agents, to spread infection
        """
        # iterate through all agents in 3 unit radius neighbourhood
        for agent in self.model.grid.iter_cell_list_contents(self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=True,
                radius=params.params['infection_radius'])):
            # we can only infect susceptible individuals
            if agent.state == InfectionState.SUS and self.random.uniform(0, 1) < \
                    params.infection_chance(toroidal_distance(self.pos, agent.pos)):
                agent.infect()

    def move(self):
        """
        Moves agent randomly in Von Neumann neighbourhood
        """
        distance_to_move = params.movement_distance()
        angle = self.random.uniform(0, 2 * pi)
        cell = (self.pos[0] + round(distance_to_move * cos(angle)),
                self.pos[1] + round(distance_to_move * sin(angle)))
        # neighbours = self.model.grid.get_neighborhood(self.pos, moore=False)
        self.model.grid.move_agent(self, cell)

    def step(self):
        """
        Called every agent step, stages changes to be applied
        """
        self.move()
        if self.state == InfectionState.INF:    # every infected agent...
            self.spread()                       # spreads the infections
            self.infection_period()           # infection duration ending
        elif params.params['has_recovery_immunity'] and self.state == InfectionState.REC:
            self.recovery_timer()               # recovered agents may get susceptible again
        elif self.state == InfectionState.SUS:
            self.try_vaccination()              # susceptible agents may get vaccinated

        self.simulate_birth()
        self.simulate_death()

    def advance(self):
        """
        Applies changes staged in step()
        """

        if self.state == InfectionState.INF:
            self.infection_duration += 1
        elif self.state == InfectionState.REC:
            self.recovered_duration += 1

        if self.target_state is not None:   # return if no changes to be staged
            self.state = self.target_state  # apply state change
            self.target_state = None        # reset

        if self.give_birth:
            # initial state may be vaccinated, if it is started and with a given probability
            initial_state = InfectionState.VAC if self.model.vaccination_started and \
                self.random.uniform(0, 1) < params.params['general_vaccination_rate'] \
                else InfectionState.SUS
            # create and add the agent
            self.model.add_agent(self.model.create_agent(initial_state), self.pos)
        if self.die:
            self.model.dead_agents.append(self)

        # reset
        self.give_birth = False
        self.die = False
