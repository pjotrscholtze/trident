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

    # def create_histogram(self, data: List[tuple[any, float]], bucketNum:int,
    #     partitionRule: PartitionRule) -> List[Bucket]:
    def create_histogram(self, data: List, bucketNum:int,
        partitionRule: PartitionRule) -> List[Bucket]:
        buckets = [Bucket([]) for i in range(0, bucketNum)]
        if not data:
            return buckets

        min: float = data[0][1]
        max: float = data[len(data)-1][1]
        step: float = (max - min) / float(bucketNum)

        for d in data:
            b: int = int((d[1] - min) / step)
            if b >= bucketNum: b = bucketNum - 1
            buckets[b].data.append(d)

        return buckets
