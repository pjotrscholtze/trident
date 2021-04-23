# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.histogram.constructionAlgorithm.vOptimalSA;
from constructionAlgorithm.vOptimalSA.VOptimalState import VOptimalState

# import madgik.exareme.utils.simulatedAnnealing.State;
from simulatedAnnealing.State import State
from simulatedAnnealing.Transformation import Transformation
# import madgik.exareme.utils.simulatedAnnealing.Transformation;

# public class VOptimalTransformation implements Transformation {
class VOptimalTransformation(Transformation):

#     private static final long serialVersionUID = 1L;
#     int threshold = -1;
#     int offset = -1;

#     public VOptimalTransformation(int threshold, int offset) {
    def __init__(self, threshold:int, offset:int):
#         this.threshold = threshold;
        self.threshold = threshold
#         this.offset = offset;
        self.offset = offset
#     }

#     public State apply(State state) {
    def apply(self, state: State) -> State:
#         VOptimalState vos = (VOptimalState) state;
        vos: VOptimalState = state
#         vos.thresholds[threshold] += offset;
        vos.thresholds[self.threshold] += self.offset
#         return vos;
        return vos
#     }
# }
