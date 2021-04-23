# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
import statistics
# package madgik.exareme.utils.histogram.score;
from score.HistogramScore import HistogramScore
# import madgik.exareme.utils.association.Pair;
# import madgik.exareme.utils.histogram.Bucket;
# import org.apache.commons.math.stat.descriptive.DescriptiveStatistics;

# import java.util.LinkedList;
from typing import List
from Bucket import Bucket
# /**
#  * @author herald
#  */
# public class MinimizeVarianceHistogramScore implements HistogramScore {
class MinimizeVarianceHistogramScore(HistogramScore):

#     public static MinimizeVarianceHistogramScore instance = new MinimizeVarianceHistogramScore();
    instance = None # type: MinimizeVarianceHistogramScore()
    
    @staticmethod
    def get_instance():
        if MinimizeVarianceHistogramScore.instance is None:
            MinimizeVarianceHistogramScore.instance = MinimizeVarianceHistogramScore()
        return MinimizeVarianceHistogramScore.instance

#     public double getScore(LinkedList<Bucket> bucketList) {
    def getScore(self, bucketList: List[Bucket]) -> float:
#         DescriptiveStatistics stats = new DescriptiveStatistics();
        stats:List[float] = []

#         for (Bucket b : bucketList) {
        for b in bucketList:
#             DescriptiveStatistics bs = new DescriptiveStatistics();
            bs:List[float] = []
            for d in b.data:
                bs.append(d[1])
#             for (Pair<?, Double> d : b.data) {
#                 bs.addValue(d.b);
#             }
            if len(bs) == 1:
                stats.append(bs[0])
                continue
            if bs:
                stats.append(statistics.stdev(bs))
                continue
            

#             stats.addValue(bs.getStandardDeviation());
#         }

#         return -stats.getStandardDeviation();
        if len(stats) == 1: return stats[0]
        return statistics.stdev(stats)
#     }
# }
