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

    def __init__(self, maxSteps: int, stepsNotImprovedTermination: int,
        temperature: Temperature):
        self.maxSteps = maxSteps
        self.stepsNotImprovedTermination = stepsNotImprovedTermination
        self.temperature = temperature

    def getInitial(self) -> State:
        """
        :return: Initial state.
        """
        raise NotImplementedError()

    def getNeighbor(self, state: State, rand: Random) -> tuple[Transformation, Transformation]:
        """
        :return: A pair with two transformations A and B with the following
                properties:
                - A: A(state) -> new state
                - B: B(A(state)) -> state
        """
        raise NotImplementedError()

    def search(self) -> State:
        bestState: State = self.getInitial()
        state:State = bestState.clone()

        rand:Random = Random()

        lastBestStep:int = 0
        for k in range(0, self.maxSteps):
            if k - lastBestStep > self.stepsNotImprovedTermination: break

            neighbor: tuple[Transformation, Transformation] = self.getNeighbor(state, rand)
            cost:float = state.getCost()
            state = neighbor[0].apply(state)

            # Always keep a better state.
            if bestState.getCost() > state.getCost():
                bestState = state.clone()
                lastBestStep = k
            else:
                # Keep the solution with a probability.
                if self.propability(cost, state.getCost(), self.temperature.getTemperature(k)) <= rand.random():
                    # Do not accept the solution.
                    state = neighbor[1].apply(state)

        return bestState

    def propability(self, cost: float, newCost: float, temperature: float) -> float:
        if newCost < cost: return 1.0
        return math.pow(math.e, -(1) / temperature)
