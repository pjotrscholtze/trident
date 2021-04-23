# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from typing import List
import logging
logging.basicConfig(level=logging.DEBUG)
from bucketNumberGenerator import BucketNumberGenerator
from bucketNumberGenerator.LinearBucketNumberGenerator import LinearBucketNumberGenerator
from constructionAlgorithm.ConstructionAlgorithm import ConstructionAlgorithm
from constructionAlgorithm.ConstructionAlgorithmFactory import ConstructionAlgorithmFactory
from partitionRule.PartitionRule import PartitionRule
from partitionRule.PartitionClass import PartitionClass
from partitionRule.PartitionConstraint import PartitionConstraint
from score.HistogramScore import HistogramScore
from score.MinimizeVarianceHistogramScore import MinimizeVarianceHistogramScore
from score.BalanceVarianceAndBucketsHistogramScore import BalanceVarianceAndBucketsHistogramScore

from Bucket import Bucket

# /**
#  * @author herald
#  */
class Histogram:

    def __init__(self, partition_rule: PartitionRule):
        self.partition_rule = partition_rule
        self.algorithm: ConstructionAlgorithm = ConstructionAlgorithmFactory.getAlgorithm(partition_rule)

#     /**
#      * @param data      the dataset with <key,value> pairs
#      * @param bucketNum the number of buckets
#      * @return a list of buckets
#      * @throws RemoteException in case of exception
#      */
    def createHistogram(self, data: List[tuple[any,float]],
        bucketNum: int = None, score: HistogramScore = None,
        generator: BucketNumberGenerator= None) -> List[Bucket]:
        if bucketNum is not None:
            return self.algorithm.createHistogram(data, bucketNum, self.partition_rule)

#     /**
#      * @param data
#      * @param score
#      * @param generator
#      * @return the histogram with the maximum score
#      * @throws RemoteException
#      */
        best:List[Bucket] = None
        bestScore: float = 0
        while generator.hasNext():
            next:int = generator.getNext()
            if best is None:
                best = self.algorithm.createHistogram(data, next, self.partition_rule)
                bestScore = score.getScore(best)
                continue

            h:List[Bucket] = self.algorithm.createHistogram(data, next, self.partition_rule)
            s:float = score.getScore(h)

            logging.debug(str(bestScore) + "(" + str(len(best)) + ")" + " >=? " + str(s) + "(" + str(next) + ")")

            if s > bestScore:
                best = h
                bestScore = s

        return best


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


