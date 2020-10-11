from utility import InfectionState, sqr_euler_distance
from mesa import Agent, Model
import simulation_parameters as params


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
        if p < params.recovery_probability:  # if agent recovers
            self.model.statistics["total_recoveries"] += 1
            if params.recovered_duration == 0:  # if there is no immunity stage
                # agents go back to susceptibility
                self.target_state = InfectionState.SUS
            else:   # otherwise, they will go to the recovery state
                self.target_state = InfectionState.REC
                self.recovery_timeout = params.recovered_duration
        elif p < params.recovery_probability + params.mortality_rate:  # if agent dies
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
