# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from typing import List
from partitionRule.PartitionRule import PartitionRule
from Bucket import Bucket

# /**
#  * Given a particular partition rule, this is the algorithm
#  * that constructs histograms that satisfy the rule. It
#  * is often the case that, for the same histogram class,
#  * there are several construction algorithms with different efficiency.
#  * [The History of Histograms Yannis Ioannidis]
#  *
#  * @author herald
#  */
class ConstructionAlgorithm:
    # def create_histogram(self, data: List[tuple[any, float]], bucketNum: int,
    #     partitionRule: PartitionRule) -> List[Bucket]: raise NotImplementedError
    def create_histogram(self, data: List, bucketNum: int,
        partitionRule: PartitionRule) -> List[Bucket]: raise NotImplementedError
