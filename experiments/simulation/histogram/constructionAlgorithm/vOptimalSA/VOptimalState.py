# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.histogram.constructionAlgorithm.vOptimalSA;

# import madgik.exareme.utils.association.Pair;
# import madgik.exareme.utils.simulatedAnnealing.State;
from simulatedAnnealing.State import State
# import org.apache.commons.math.stat.descriptive.DescriptiveStatistics;
import statistics, math


# import java.util.ArrayList;
from typing import List

# public class VOptimalState implements State {
class VOptimalState(State):
    pass

#     private static final long serialVersionUID = 1L;
#     public int[] thresholds = null;
#     private ArrayList<Pair<?, Double>> data = null;

#     public VOptimalState(ArrayList<Pair<?, Double>> data, int[] thresholds) {
    def __init__(self, data: List[tuple[any,float]], thresholds: List[int]):
#         this.data = data;
        self.data = data
#         this.thresholds = thresholds;
        self.thresholds = thresholds
#     }

#     public double getCost() {
    def getCost(self) -> float:
#         double cost = 0;
        cost: float = 0

#         int prev = 0;
        prev: int = 0
#         for (int t : thresholds) {
        for t in self.thresholds:
#             DescriptiveStatistics stats = new DescriptiveStatistics();
            stats = []
#             for (int i = prev; i < t; i++) {
            for i in range(prev, t):
#                 stats.addValue(data.get(i).b);
                stats.append(self.data[i][1])
#             }
#             cost += stats.getN() * stats.getVariance();
            if len(stats) > 1: cost += len(stats) * statistics.variance(stats)
#             prev = t;
            prev = t
#         }

# 	/* last bucket */
#         DescriptiveStatistics stats = new DescriptiveStatistics();
        stats = []
#         int max = data.size();
        max:int = len(self.data)
#         for (int i = prev; i < max; i++) {
        for i in range(prev, max):
#             stats.addValue(data.get(i).b);
            stats.append(self.data[i][1])
#         }
#         cost += stats.getN() * stats.getVariance();
        if len(stats) > 1: cost += len(stats) * statistics.variance(stats)

#         return cost;
        return cost
#     }

#     @Override public State clone() {
    def clone(self) -> State:
#         int[] newThresholds = new int[thresholds.length];
#         System.arraycopy(thresholds, 0, newThresholds, 0, newThresholds.length);
#         return new VOptimalState(data, newThresholds);
        return VOptimalState(self.data, [] + self.thresholds)
#     }
# }
