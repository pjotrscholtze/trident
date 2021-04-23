# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.histogram.constructionAlgorithm.vOptimalSA;
from constructionAlgorithm.vOptimalSA.VOptimalState import VOptimalState
from constructionAlgorithm.vOptimalSA.VOptimalTransformation import VOptimalTransformation

# import madgik.exareme.utils.association.Pair;
# import madgik.exareme.utils.simulatedAnnealing.SimulatedAnnealing;
from simulatedAnnealing.SimulatedAnnealing import SimulatedAnnealing
# import madgik.exareme.utils.simulatedAnnealing.State;
from simulatedAnnealing.State import State
# import madgik.exareme.utils.simulatedAnnealing.Temperature;
from simulatedAnnealing.Temperature import Temperature
# import madgik.exareme.utils.simulatedAnnealing.Transformation;
from simulatedAnnealing.Transformation import Transformation

# import java.rmi.RemoteException;
# import java.util.ArrayList;
from typing import List
# import java.util.Random;
from random import Random

# public class VOptimalSA extends SimulatedAnnealing {
class VOptimalSA(SimulatedAnnealing):

#     private static final long serialVersionUID = 1L;
#     private ArrayList<Pair<?, Double>> data = null;
#     private int bucketNum = 0;

#     public VOptimalSA(int maxSteps, int stepsNotImprovedTermination, Temperature temperature,
#         ArrayList<Pair<?, Double>> data, int bucketNum) {
    def __init__(self, maxSteps:int, stepsNotImprovedTermination:int, temperature: Temperature,
        data: List[tuple[any,float]], bucketNum:int):
#         super(maxSteps, stepsNotImprovedTermination, temperature);
        super(VOptimalSA, self).__init__(maxSteps,stepsNotImprovedTermination, temperature)

#         this.data = data;
        self.data = data
#         this.bucketNum = bucketNum;
        self.bucketNum = bucketNum
#     }

#     @Override public State getInitial() throws RemoteException {
    def getInitial(self) -> State:
#         int[] thresholds = new int[bucketNum - 1];
        thresholds: List[int] = []

#     /* Initialize thresholds */
#         int step = data.size() / bucketNum;
        step:int = int(len(self.data) / self.bucketNum)
#         for (int i = 0; i < thresholds.length; i++) {
        for i in range(0, self.bucketNum):
#             thresholds[i] = (i + 1) * step;
            thresholds.append((i + 1) * step)
#         }

#         return new VOptimalState(data, thresholds);
        return VOptimalState(self.data, thresholds)
#     }

#     @Override public Pair<Transformation, Transformation> getNeighbor(State state, Random rand)
#         throws RemoteException {
    def getNeighbor(self, state: State, rand: Random) -> tuple[Transformation, Transformation]:
#         VOptimalState vos = (VOptimalState) state;
        vos:VOptimalState = state

#         int threshold = 0;
        threshold:int = 0
#         int offset = 0;
        offset:int = 0

#         while (true) {
        while True:
#       /* Peek a random threshold */
#             threshold = rand.nextInt(bucketNum - 1);
            threshold = rand.randint(0, self.bucketNum - 1)
#             int leftOffset = 0;
            leftOffset:int = 0
#             int rightOffset = 0;
            rightOffset:int = 0

#             if (threshold == 0) {
            if threshold == 0:
#                 leftOffset = vos.thresholds[threshold] - 1;
                leftOffset = vos.thresholds[threshold] - 1
#             } else {
            else:
#                 leftOffset = vos.thresholds[threshold] - vos.thresholds[threshold - 1] - 1;
                leftOffset = vos.thresholds[threshold] - vos.thresholds[threshold - 1] - 1
#             }

#             if (threshold == bucketNum - 2) {
            if threshold >= self.bucketNum - 2:
#                 rightOffset = data.size() - vos.thresholds[threshold] - 1;
                rightOffset = len(self.data) - vos.thresholds[threshold] - 1
#             } else {
            else:
#                 rightOffset = vos.thresholds[threshold + 1] - vos.thresholds[threshold] - 1;
                rightOffset = vos.thresholds[threshold + 1] - vos.thresholds[threshold] - 1
#             }

#             if (leftOffset > 0 || rightOffset > 0) {
            if leftOffset > 0 or rightOffset > 0:
#                 if (rand.nextBoolean()) {
                if rand.randint(0, 1) == 1:
#                     if (leftOffset > 0) {
                    if leftOffset > 0:
#                         offset = -1;
                        offset = -1
#                     } else {
                    else:
#                         offset = 1;
                        offset = 1
#                     }
#                 } else {
                else:
#                     if (rightOffset > 0) {
                    if rightOffset > 0:
#                         offset = 1;
                        offset = 1
#                     } else {
                    else:
#                         offset = -1;
                        offset = -1
#                     }
#                 }

#                 break;
                break
#             }
#         }

#         Transformation t1 = new VOptimalTransformation(threshold, offset);
        t1:Transformation = VOptimalTransformation(threshold, offset)
#         Transformation t2 = new VOptimalTransformation(threshold, -offset);
        t2:Transformation = VOptimalTransformation(threshold, -offset)

#         return new Pair<Transformation, Transformation>(t1, t2);
        return t1, t2
#     }
# }
