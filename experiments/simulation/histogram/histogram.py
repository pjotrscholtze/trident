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
        self.algorithm: ConstructionAlgorithm = ConstructionAlgorithmFactory.get_algorithm(partition_rule)

    def create_histogram(self, data: List[tuple[any,float]],
        bucketNum: int = None, score: HistogramScore = None,
        generator: BucketNumberGenerator= None) -> List[Bucket]:
        """
        :param: data:      The dataset with <key,value> pairs.
        :param: bucketNum: The number of buckets (option 1).
        :param: score:     (option 2).
        :param: generator: (option 2).
        :return: A list of buckets (option 1). The histogram with the maximum
                 score (option 2).
        """
        if bucketNum is not None:
            return self.algorithm.create_histogram(data, bucketNum, self.partition_rule)

        best: List[Bucket] = None
        bestScore: float = 0
        while generator.has_next():
            next: int = generator.get_next()
            if best is None:
                best = self.algorithm.create_histogram(data, next, self.partition_rule)
                bestScore = score.get_score(best)
                continue

            h: List[Bucket] = self.algorithm.create_histogram(data, next, self.partition_rule)
            s: float = score.get_score(h)

            logging.debug(str(bestScore) + "(" + str(len(best)) + ")" + " >=? " + str(s) + "(" + str(next) + ")")

            if s > bestScore:
                best = h
                bestScore = s

        return best


if __name__ == "__main__":
    import json
    hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.maxdiff))
    test = hist.create_histogram([
        [1, 2],
        [1, 2],
        [10, 2],
        [100, 1],
    ], 2)
    print(json.dumps([e.data for e in test], indent=2))
    test = hist.create_histogram([
        [1, 2],
        [1, 2],
        [10, 2],
        [100, 1],
    ], score= MinimizeVarianceHistogramScore(),
        generator= LinearBucketNumberGenerator(0, 1, 10))
    print(json.dumps([e.data for e in test], indent=2))
    test = hist.create_histogram([
        [1, 2],
        [1, 2],
        [10, 2],
        [100, 1],
    ], score= BalanceVarianceAndBucketsHistogramScore(1),
        generator= LinearBucketNumberGenerator(0, 1, 10))
    print(json.dumps([e.data for e in test], indent=2))

    print("----")
    print("----")
    print("----")

    hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.equi_width))
    test = hist.create_histogram([
        [1, 2],
        [1, 2],
        [10, 2],
        [100, 1],
    ], 2)
    print(json.dumps([e.data for e in test], indent=2))
    test = hist.create_histogram([
        [1, 2],
        [1, 2],
        [10, 2],
        [100, 1],
    ], score= MinimizeVarianceHistogramScore(),
        generator= LinearBucketNumberGenerator(1, 1, 10))
    print(json.dumps([e.data for e in test], indent=2))
    test = hist.create_histogram([
        [1, 2],
        [1, 2],
        [10, 2],
        [100, 1],
    ], score= BalanceVarianceAndBucketsHistogramScore(1),
        generator= LinearBucketNumberGenerator(1, 1, 10))

    print("----")
    print("----")
    print("----")

    hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.v_optimal))
    test = hist.create_histogram([
        [1, 2],
        [1, 2],
        [10, 2],
        [100, 1],
    ], 2)
    print(json.dumps([e.data for e in test], indent=2))
    # test = hist.create_histogram([
    #     [1,2],
    #     [1,2],
    #     [10,2],
    #     [100,1],
    # ], score= MinimizeVarianceHistogramScore(),
    #     generator= LinearBucketNumberGenerator(1, 1, 10))
    # print(json.dumps([e.data for e in test], indent=2))
    # test = hist.create_histogram([
    #     [1,2],
    #     [1,2],
    #     [10,2],
    #     [100,1],
    # ], score= BalanceVarianceAndBucketsHistogramScore(1),
    #     generator= LinearBucketNumberGenerator(1, 1, 10))
    # print(json.dumps([e.data for e in test], indent=2))


