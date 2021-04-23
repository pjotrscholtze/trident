# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */

from constructionAlgorithm.ConstructionAlgorithm import ConstructionAlgorithm
from Bucket import Bucket
from partitionRule.PartitionRule import PartitionRule

from typing import List

# /**
#  * @author herald
#  */
class EquiWidthConstructionAlgorithm(ConstructionAlgorithm):

    def createHistogram(self, data: List[tuple[any, float]], bucketNum:int,
        partitionRule: PartitionRule) -> List[Bucket]:
        if not data:
            bucket_list = []
            for i in range(0, bucketNum):
                bucket_list.append(Bucket([]))
            return bucket_list
        min: float = data[0][1]
        max: float = data[len(data)-1][1]
        step: float = (max - min) / float(bucketNum)

        buckets = []
        for i in range(0, bucketNum):
            buckets.append([])

        for d in data:
            b: int = int((d[1] - min) / step)
            if b == bucketNum: b -= 1
            buckets[b].append(d)
        bucketList = []
        for bData in buckets:
            bucketList.append(Bucket(bData))
        return bucketList
