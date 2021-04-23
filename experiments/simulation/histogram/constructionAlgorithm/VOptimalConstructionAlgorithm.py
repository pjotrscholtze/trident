# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from typing import List
from constructionAlgorithm.ConstructionAlgorithm import ConstructionAlgorithm

from Bucket import Bucket
from constructionAlgorithm.vOptimalSA.VOptimalSA import VOptimalSA
from constructionAlgorithm.vOptimalSA.VOptimalState import VOptimalState
from partitionRule.PartitionRule import PartitionRule
from simulatedAnnealing.LogarithmicTemperature import LogarithmicTemperature


# /**
#  * @author herald
#  */
class VOptimalConstructionAlgorithm(ConstructionAlgorithm):

    def createHistogram(self, data: List[tuple[any,float]], bucketNum: int,
        partitionRule: PartitionRule) -> List[Bucket]:

        if bucketNum < 1: raise AttributeError("Bucket num should be > 0")

        bucketList:List[Bucket] = []

        # Put everything into 1 bucket.
        if bucketNum == 1: return [Bucket(data)]

        sa = VOptimalSA(10000, 1000, LogarithmicTemperature(1.0), data, bucketNum)
        result: VOptimalState = sa.search()
        index: int = 0
        for t in result.thresholds:
            b = Bucket(data[index: t])
            bucketList.append(b)
            index = t

        b: Bucket = Bucket(data[index:len(data)])
        bucketList.append(b)
        return bucketList
