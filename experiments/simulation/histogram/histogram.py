# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.histogram;
from typing import List
import logging
logging.basicConfig(level=logging.DEBUG)
# import madgik.exareme.utils.association.Pair;
# import madgik.exareme.utils.histogram.bucketNumberGenerator.BucketNumberGenerator;
from bucketNumberGenerator import BucketNumberGenerator
from bucketNumberGenerator.LinearBucketNumberGenerator import LinearBucketNumberGenerator
# import madgik.exareme.utils.histogram.constructionAlgorithm.ConstructionAlgorithm;
from constructionAlgorithm.ConstructionAlgorithm import ConstructionAlgorithm
# import madgik.exareme.utils.histogram.constructionAlgorithm.ConstructionAlgorithmFactory;
from constructionAlgorithm.ConstructionAlgorithmFactory import ConstructionAlgorithmFactory
# import madgik.exareme.utils.histogram.partitionRule.PartitionRule;
from partitionRule.PartitionRule import PartitionRule
from partitionRule.PartitionClass import PartitionClass
from partitionRule.PartitionConstraint import PartitionConstraint
# import madgik.exareme.utils.histogram.score.HistogramScore;
from score.HistogramScore import HistogramScore
from score.MinimizeVarianceHistogramScore import MinimizeVarianceHistogramScore
from score.BalanceVarianceAndBucketsHistogramScore import BalanceVarianceAndBucketsHistogramScore
# import org.apache.log4j.Logger;

# import java.rmi.RemoteException;
# import java.util.ArrayList;
# import java.util.LinkedList;
from Bucket import Bucket
# /**
#  * @author herald
#  */
# public class Histogram {
class Histogram:
#     private static Logger log = Logger.getLogger(Histogram.class);
#     private PartitionRule partitionRule = null;
#     private ConstructionAlgorithm algorithm = null;
#     //    private FrequencyApproximation frequencyApproximation = null;
#     //    private ValueApproximation valueApproximation = null;

    def __init__(self, partition_rule: PartitionRule):
        self.partition_rule = partition_rule
        self.algorithm: ConstructionAlgorithm = ConstructionAlgorithmFactory.getAlgorithm(partition_rule)
#     public Histogram(PartitionRule partitionRule) {
#         this.partitionRule = partitionRule;
#         this.algorithm = ConstructionAlgorithmFactory.getAlgorithm(partitionRule);
#         //	this.frequencyApproximation = frequencyApproximation;
#         //	this.valueApproximation = valueApproximation;
#     }

#     /**
#      * @param data      the dataset with <key,value> pairs
#      * @param bucketNum the number of buckets
#      * @return a list of buckets
#      * @throws RemoteException in case of exception
#      */
#     public LinkedList<Bucket> createHistogram(ArrayList<Pair<?, Double>> data, int bucketNum)
#         throws RemoteException {
    def createHistogram(self, data: List[tuple[any,float]],
        bucketNum: int = None, score: HistogramScore = None,
        generator: BucketNumberGenerator= None) -> List[Bucket]:
        if bucketNum is not None:
            return self.algorithm.createHistogram(data, bucketNum, self.partition_rule)

#         LinkedList<Bucket> bucketList = algorithm.createHistogram(data, bucketNum, partitionRule);
#     /* TODO: approximate value and frequency */
#         return bucketList;
#     }

#     /**
#      * @param data
#      * @param score
#      * @param generator
#      * @return the histogram with the maximum score
#      * @throws RemoteException
#      */
#     public LinkedList<Bucket> createHistogram(ArrayList<Pair<?, Double>> data, HistogramScore score,
#         BucketNumberGenerator generator) throws RemoteException {
    # def createHistogram(self, data: List[tuple[any,float]], score: HistogramScore = None,
    #     generator: BucketNumberGenerator= None) -> List[Bucket]:
        # pass

#         LinkedList<Bucket> best = null;
        best:List[Bucket] = None
#         double bestScore = 0;
        bestScore: float = 0

#         while (generator.hasNext()) {
        while generator.hasNext():
#             int next = generator.getNext();
            next:int = generator.getNext()

#             if (best == null) {
            if best is None:
#                 best = algorithm.createHistogram(data, next, partitionRule);
                best = self.algorithm.createHistogram(data, next, self.partition_rule)
#                 bestScore = score.getScore(best);
                bestScore = score.getScore(best)
#                 continue;
                continue
#             }

#             LinkedList<Bucket> h = algorithm.createHistogram(data, next, partitionRule);
            h:List[Bucket] = self.algorithm.createHistogram(data, next, self.partition_rule)
#             double s = score.getScore(h);
            s:float = score.getScore(h)

#             log.debug(bestScore + "(" + best.size() + ")" + " >=? " + s + "(" + next + ")");
            logging.debug(str(bestScore) + "(" + str(len(best)) + ")" + " >=? " + str(s) + "(" + str(next) + ")")

#             if (s > bestScore) {
            if s > bestScore:
#                 best = h;
                best = h
#                 bestScore = s;
                bestScore = s
#             }
#         }

#         return best;
        return best
#     }
# }


if __name__ == "__main__":
    import json
    hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.maxdiff))
    test = hist.createHistogram([
        [1,2],
        [1,2],
        [10,2],
        [100,1],
    ],2)
    print(json.dumps([e.data for e in test], indent=2))
    test = hist.createHistogram([
        [1,2],
        [1,2],
        [10,2],
        [100,1],
    ], score= MinimizeVarianceHistogramScore(),
        generator= LinearBucketNumberGenerator(0, 1, 10))
    print(json.dumps([e.data for e in test], indent=2))
    test = hist.createHistogram([
        [1,2],
        [1,2],
        [10,2],
        [100,1],
    ], score= BalanceVarianceAndBucketsHistogramScore(1),
        generator= LinearBucketNumberGenerator(0, 1, 10))
    print(json.dumps([e.data for e in test], indent=2))

    print("----")
    print("----")
    print("----")

    hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.equi_width))
    test = hist.createHistogram([
        [1,2],
        [1,2],
        [10,2],
        [100,1],
    ],2)
    print(json.dumps([e.data for e in test], indent=2))
    test = hist.createHistogram([
        [1,2],
        [1,2],
        [10,2],
        [100,1],
    ], score= MinimizeVarianceHistogramScore(),
        generator= LinearBucketNumberGenerator(1, 1, 10))
    print(json.dumps([e.data for e in test], indent=2))
    test = hist.createHistogram([
        [1,2],
        [1,2],
        [10,2],
        [100,1],
    ], score= BalanceVarianceAndBucketsHistogramScore(1),
        generator= LinearBucketNumberGenerator(1, 1, 10))

    print("----")
    print("----")
    print("----")

    hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.v_optimal))
    test = hist.createHistogram([
        [1,2],
        [1,2],
        [10,2],
        [100,1],
    ],2)
    print(json.dumps([e.data for e in test], indent=2))
    # test = hist.createHistogram([
    #     [1,2],
    #     [1,2],
    #     [10,2],
    #     [100,1],
    # ], score= MinimizeVarianceHistogramScore(),
    #     generator= LinearBucketNumberGenerator(1, 1, 10))
    # print(json.dumps([e.data for e in test], indent=2))
    # test = hist.createHistogram([
    #     [1,2],
    #     [1,2],
    #     [10,2],
    #     [100,1],
    # ], score= BalanceVarianceAndBucketsHistogramScore(1),
    #     generator= LinearBucketNumberGenerator(1, 1, 10))
    # print(json.dumps([e.data for e in test], indent=2))


