# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.simulatedAnnealing;
from simulatedAnnealing.Transformation import Transformation
from simulatedAnnealing.Temperature import Temperature
from simulatedAnnealing.State import State

# import madgik.exareme.utils.association.Pair;

# import java.io.Serializable;
# import java.rmi.RemoteException;
# import java.util.Random;
from random import Random

import math
# /**
#  * @author herald
#  */
# public abstract class SimulatedAnnealing implements Serializable {
class SimulatedAnnealing:

#     private static final long serialVersionUID = 1L;
#     private int maxSteps = 0;
#     private int stepsNotImprovedTermination = 0;
#     private Temperature temperature = null;

#     public SimulatedAnnealing(int maxSteps, int stepsNotImprovedTermination,
    def __init__(self, maxSteps: int, stepsNotImprovedTermination: int,
        temperature: Temperature):
#         Temperature temperature) {
#         this.maxSteps = maxSteps;
        self.maxSteps = maxSteps
#         this.stepsNotImprovedTermination = stepsNotImprovedTermination;
        self.stepsNotImprovedTermination = stepsNotImprovedTermination
#         this.temperature = temperature;
        self.temperature = temperature
#     }

#     /* return: initial state */
#     public abstract State getInitial() throws RemoteException;
    def getInitial(self) -> State: raise NotImplementedError()

#     /*
#      * return: a pair with two transformations A and B with
#      * the following properties:
#      *  A: A(state) -> new state
#      *  B: B(A(state)) -> state
#      */
#     public abstract Pair<Transformation, Transformation> getNeighbor(State state, Random rand)
#         throws RemoteException;
    def getNeighbor(self, state: State, rand: Random) -> tuple[Transformation, Transformation]: raise NotImplementedError()

#     public State search() throws RemoteException {
    def search(self) -> State:
        bestState: State = self.getInitial()
        state:State = bestState.clone()

        rand:Random = Random()

#         long lastBestStep = 0;
        lastBestStep:int = 0
#         for (int k = 0; k < maxSteps; k++) {
        for k in range(0, self.maxSteps):
#             if (k - lastBestStep > stepsNotImprovedTermination) {
            if k - lastBestStep > self.stepsNotImprovedTermination:
#                 break;
                break
#             }

#             Pair<Transformation, Transformation> neighbor = getNeighbor(state, rand);
            neighbor: tuple[Transformation, Transformation] = self.getNeighbor(state, rand)

#             double cost = state.getCost();
            cost:float = state.getCost()
#             state = neighbor.a.apply(state);
            state = neighbor[0].apply(state)

#       /* Always keep a better state */
#             if (bestState.getCost() > state.getCost()) {
            if bestState.getCost() > state.getCost():
#                 bestState = state.clone();
                bestState = state.clone()

#                 lastBestStep = k;
                lastBestStep = k
#             } else {
            else:
#         /* Keep the solution with a probability */
#                 if (propability(cost, state.getCost(), temperature.getTemperature(k)) <= rand
#                     .nextDouble()) {
                if self.propability(cost, state.getCost(), self.temperature.getTemperature(k)) <= rand.random():
#           /* do not accept the solution */
#                     state = neighbor.b.apply(state);
                    state = neighbor[1].apply(state)
#                 }
#             }
#         }

#         return bestState;
        return bestState
#     }

#     public double propability(double cost, double newCost, double temperature)
    def propability(self, cost: float, newCost: float, temperature: float) -> float:
#         throws RemoteException {
#         if (newCost < cost) {
        if newCost < cost: return 1.0
#             return 1.0;
#         }

#         double prop = Math.pow(Math.E, -(1) / temperature);
#         return prop;
        return math.pow(math.e, -(1) / temperature)
#     }
# }
