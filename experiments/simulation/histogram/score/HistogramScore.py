# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.histogram.score;

# import madgik.exareme.utils.histogram.Bucket;
from Bucket import Bucket
# import java.util.LinkedList;
from typing import List

# /**
#  * @author herald
#  */
# public interface HistogramScore {
class HistogramScore:
    def getScore(self, bucketList: List[Bucket]): raise NotImplementedError()

#     double getScore(LinkedList<Bucket> bucketList);
# }
