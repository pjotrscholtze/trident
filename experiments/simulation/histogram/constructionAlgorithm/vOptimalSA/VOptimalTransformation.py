# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from constructionAlgorithm.vOptimalSA.VOptimalState import VOptimalState

from simulatedAnnealing.State import State
from simulatedAnnealing.Transformation import Transformation

class VOptimalTransformation(Transformation):

    def __init__(self, threshold:int, offset:int):
        self.threshold = threshold
        self.offset = offset

    def apply(self, state: State) -> State:
        vos: VOptimalState = state
        vos.thresholds[self.threshold] += self.offset
        return vos
