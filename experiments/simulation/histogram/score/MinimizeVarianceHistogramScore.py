# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
import statistics
from score.HistogramScore import HistogramScore

from typing import List
from Bucket import Bucket
# /**
#  * @author herald
#  */
class MinimizeVarianceHistogramScore(HistogramScore):
    instance = None # type: MinimizeVarianceHistogramScore()
    
    @staticmethod
    def get_instance():
        if MinimizeVarianceHistogramScore.instance is None:
            MinimizeVarianceHistogramScore.instance = MinimizeVarianceHistogramScore()
        return MinimizeVarianceHistogramScore.instance

    def getScore(self, bucketList: List[Bucket]) -> float:
        stats:List[float] = []

        for b in bucketList:
            bs:List[float] = []
            for d in b.data:
                bs.append(d[1])
            if len(bs) == 1:
                stats.append(bs[0])
                continue
            if bs:
                stats.append(statistics.stdev(bs))
                continue

        if len(stats) == 1: return stats[0]
        return statistics.stdev(stats)
