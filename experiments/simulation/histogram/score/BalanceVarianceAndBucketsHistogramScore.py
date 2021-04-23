# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
import statistics
# package madgik.exareme.utils.histogram.score;
from score.HistogramScore import HistogramScore

# import madgik.exareme.utils.association.Pair;
# import madgik.exareme.utils.histogram.Bucket;
from Bucket import Bucket
# import org.apache.commons.math.stat.descriptive.DescriptiveStatistics;
# import java.util.LinkedList;
from typing import List

# /**
#  * @author herald
#  */
# public class BalanceVarianceAndBucketsHistogramScore implements HistogramScore {
class BalanceVarianceAndBucketsHistogramScore(HistogramScore):
    pass

#     public double a = 0.0;
#     public BalanceVarianceAndBucketsHistogramScore(double a) {
#         this.a = a;
#     }
    def __init__(self, a: float): self.a = a

#     public double getScore(LinkedList<Bucket> bucketList) {
    def getScore(self, bucketList: List[Bucket]):
#         DescriptiveStatistics stats = new DescriptiveStatistics();
        stats = []

#         for (Bucket b : bucketList) {
        for b in bucketList:
#             DescriptiveStatistics bs = new DescriptiveStatistics();
            bs = []
#             for (Pair<?, Double> d : b.data) {
            for d in b.data:
#                 bs.addValue(d.b);
                bs.append(d[1])
#             }
            if not bs: continue

#             stats.addValue(bs.getStandardDeviation());
            val = bs[0]
            if len(bs) > 1: val = statistics.stdev(bs)
            stats.append(val)
#         }

        stats_std = stats[0]
        if len(stats) > 1: stats_std = statistics.stdev(stats)
#         return -(a * stats.getStandardDeviation() + (1.0 - a) * bucketList.size());
        return -(self.a * stats_std + (1.0 - self.a) * len(bucketList))
#     }
# }
