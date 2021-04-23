# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
import statistics
from score.HistogramScore import HistogramScore

from Bucket import Bucket
from typing import List

# /**
#  * @author herald
#  */
class BalanceVarianceAndBucketsHistogramScore(HistogramScore):


    def __init__(self, a: float): self.a = a


    def get_score(self, bucketList: List[Bucket]):
        stats = []
        for b in bucketList:
            bs = []
            for d in b.data:
                bs.append(d[1])
            if not bs: continue

            val = bs[0]
            if len(bs) > 1: val = statistics.stdev(bs)
            stats.append(val)

        stats_std = stats[0]
        if len(stats) > 1: stats_std = statistics.stdev(stats)
        return -(self.a * stats_std + (1.0 - self.a) * len(bucketList))
