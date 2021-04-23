# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from simulatedAnnealing.Transformation import Transformation
from simulatedAnnealing.Temperature import Temperature
from simulatedAnnealing.State import State

from random import Random

import math
# /**
#  * @author herald
#  */
class SimulatedAnnealing:

    def __init__(self, max_steps: int, steps_not_improved_termination: int,
        temperature: Temperature):
        self.max_steps = max_steps
        self.steps_not_improved_termination = steps_not_improved_termination
        self.temperature = temperature

    def get_initial(self) -> State:
        """
        :return: Initial state.
        """
        raise NotImplementedError()

    def get_neighbor(self, state: State, rand: Random) -> tuple[Transformation, Transformation]:
        """
        :return: A pair with two transformations A and B with the following
                properties:
                - A: A(state) -> new state
                - B: B(A(state)) -> state
        """
        raise NotImplementedError()

    def search(self) -> State:
        bestState: State = self.get_initial()
        state:State = bestState.clone()

        rand:Random = Random()

        lastBestStep:int = 0
        for k in range(0, self.max_steps):
            if k - lastBestStep > self.steps_not_improved_termination: break

            neighbor: tuple[Transformation, Transformation] = self.get_neighbor(state, rand)
            cost:float = state.get_cost()
            state = neighbor[0].apply(state)

            # Always keep a better state.
            if bestState.get_cost() > state.get_cost():
                bestState = state.clone()
                lastBestStep = k
            else:
                # Keep the solution with a probability.
                if self.propability(cost, state.get_cost(), self.temperature.get_temperature(k)) <= rand.random():
                    # Do not accept the solution.
                    state = neighbor[1].apply(state)

        return bestState

    def propability(self, cost: float, newCost: float, temperature: float) -> float:
        if newCost < cost: return 1.0
        return math.pow(math.e, -(1) / temperature)
