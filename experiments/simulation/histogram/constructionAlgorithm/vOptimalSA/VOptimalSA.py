# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from constructionAlgorithm.vOptimalSA.VOptimalState import VOptimalState
from constructionAlgorithm.vOptimalSA.VOptimalTransformation import VOptimalTransformation

from simulatedAnnealing.SimulatedAnnealing import SimulatedAnnealing
from simulatedAnnealing.State import State
from simulatedAnnealing.Temperature import Temperature
from simulatedAnnealing.Transformation import Transformation

from typing import List
from random import Random

class VOptimalSA(SimulatedAnnealing):

    def __init__(self, max_steps: int, steps_not_improved_termination: int, temperature: Temperature,
        data: List[tuple[any, float]], bucket_num: int):
        super(VOptimalSA, self).__init__(max_steps,steps_not_improved_termination, temperature)
        self.data = data
        self.bucket_num = bucket_num

    def get_initial(self) -> State:
        thresholds: List[int] = []

        # Initialize thresholds.
        step: int = int(len(self.data) / self.bucket_num)
        for i in range(0, self.bucket_num):
            thresholds.append((i + 1) * step)

        return VOptimalState(self.data, thresholds)

    def get_neighbor(self, state: State, rand: Random) -> tuple[Transformation, Transformation]:
        vos: VOptimalState = state
        threshold: int = 0
        offset: int = 0

        while True:
            # /* Peek a random threshold */
            threshold = rand.randint(0, self.bucket_num - 1)
            leftOffset: int = 0
            rightOffset: int = 0

            if threshold == 0:
                leftOffset = vos.thresholds[threshold] - 1
            else:
                leftOffset = vos.thresholds[threshold] - vos.thresholds[threshold - 1] - 1

            if threshold >= self.bucket_num - 2:
                rightOffset = len(self.data) - vos.thresholds[threshold] - 1
            else:
                rightOffset = vos.thresholds[threshold + 1] - vos.thresholds[threshold] - 1

            if leftOffset > 0 or rightOffset > 0:
                if rand.randint(0, 1) == 1:
                    if leftOffset > 0:
                        offset = -1
                    else:
                        offset = 1
                else:
                    if rightOffset > 0:
                        offset = 1
                    else:
                        offset = -1
                break
        t1:Transformation = VOptimalTransformation(threshold, offset)
        t2:Transformation = VOptimalTransformation(threshold, -offset)
        return t1, t2
