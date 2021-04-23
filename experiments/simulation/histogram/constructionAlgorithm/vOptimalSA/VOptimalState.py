# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */

from simulatedAnnealing.State import State
import statistics, math

from typing import List

class VOptimalState(State):
    def __init__(self, data: List[tuple[any,float]], thresholds: List[int]):
        self.data = data
        self.thresholds = thresholds

    def get_cost(self) -> float:
        cost: float = 0
        prev: int = 0
        for t in self.thresholds:
            stats = []
            for i in range(prev, t):
                stats.append(self.data[i][1])
            if len(stats) > 1: cost += len(stats) * statistics.variance(stats)
            prev = t

	# Last bucket.
        stats = []
        max: int = len(self.data)
        for i in range(prev, max): stats.append(self.data[i][1])
        if len(stats) > 1: cost += len(stats) * statistics.variance(stats)

        return cost

    def clone(self) -> State:
        return VOptimalState(self.data, [] + self.thresholds)
