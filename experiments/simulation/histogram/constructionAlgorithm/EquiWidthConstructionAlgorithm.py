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

    # def create_histogram(self, data: List[tuple[any, float]], bucket_num:int,
    #     partitionRule: PartitionRule) -> List[Bucket]:
    def create_histogram(self, data: List, bucket_num:int,
        partitionRule: PartitionRule) -> List[Bucket]:
        buckets = [Bucket([]) for i in range(0, bucket_num)]
        if not data:
            return buckets

        min_value: float = data[0][1]
        max_value: float = data[len(data)-1][1]
        step: float = (max_value - min_value) / float(bucket_num)

        for d in data:
            b: int = int(max(0, (d[1] - min_value) / step))
            if b >= bucket_num: b = bucket_num - 1
            buckets[b].data.append(d)

        return buckets
