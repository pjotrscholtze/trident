# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from constructionAlgorithm.ConstructionAlgorithm import ConstructionAlgorithm
from Bucket import Bucket
from partitionRule.PartitionRule import PartitionRule
from queue import PriorityQueue
from typing import List

# /**
#  * @author herald
#  */
class MaxDiffConstructionAlgorithm(ConstructionAlgorithm):
    def createHistogram(self, data: List[tuple[any,float]], bucketNum: int,
        partitionRule: PartitionRule) -> List[Bucket]:
        diff_queue = PriorityQueue()
        for i in range(0, len(data) - 1):
            d1 = data[i]
            d2 = data[i]
            diff_queue.put((d2[1] - d1[1], i + 1))

            if (i >= bucketNum - 1): diff_queue.get()
        bucket_list: List[Bucket] = []

        # Sort the buckets.
        thresholdArray = []
        while not diff_queue.empty(): thresholdArray.append(diff_queue.get())
        def sorter(o): return o[1]
        thresholdArray.sort(key=sorter)

        index: int = 0
        for t in thresholdArray:
            b = Bucket(data[index:t[1]])
            bucket_list.append(b)

            index = t[1]
        b = Bucket(data[index:len(data)])
        bucket_list.append(b)

        return bucket_list
