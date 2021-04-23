# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */

# package madgik.exareme.utils.histogram.constructionAlgorithm;
from constructionAlgorithm.ConstructionAlgorithm import ConstructionAlgorithm
# import madgik.exareme.utils.association.Pair;
# import madgik.exareme.utils.histogram.Bucket;
from Bucket import Bucket
# import madgik.exareme.utils.histogram.partitionRule.PartitionRule;
from partitionRule.PartitionRule import PartitionRule

# import java.rmi.RemoteException;
# import java.util.ArrayList;
from typing import List
# import java.util.LinkedList;

# /**
#  * @author herald
#  */
# public class EquiWidthConstructionAlgorithm implements ConstructionAlgorithm {
class EquiWidthConstructionAlgorithm(ConstructionAlgorithm):

#     private static final long serialVersionUID = 1L;

#     public LinkedList<Bucket> createHistogram(ArrayList<Pair<?, Double>> data, int bucketNum,
    def createHistogram(self, data: List[tuple[any, float]], bucketNum:int,
        partitionRule: PartitionRule) -> List[Bucket]:
#         if (data.isEmpty()) {
        if not data:
#             LinkedList<Bucket> bucketList = new LinkedList<Bucket>();
            bucket_list = []
#             for (int i = 0; i < bucketNum; ++i) {
            for i in range(0, bucketNum):
#                 bucketList.add(new Bucket(new LinkedList<Pair<?, Double>>()));
                bucket_list.append(Bucket([]))
#             }

#             return bucketList;
            return bucket_list
#         }

#         double min = data.get(0).b;
        min: float = data[0][1]
#         double max = data.get(data.size() - 1).b;
        max: float = data[len(data)-1][1]
#         double step = (max - min) / (double) bucketNum;
        step: float = (max - min) / float(bucketNum)

#         ArrayList<LinkedList<Pair<?, Double>>> buckets =
#             new ArrayList<LinkedList<Pair<?, Double>>>();
        buckets = []
#         for (int i = 0; i < bucketNum; ++i) {
        for i in range(0, bucketNum):
#             buckets.add(new LinkedList<Pair<?, Double>>());
            buckets.append([])
#         }

#         for (Pair<?, Double> d : data) {
        for d in data:
#             int b = (int) ((d.b - min) / step);
            b: int = int((d[1] - min) / step)
#             if (b == bucketNum) {
#                 b--;
            if b == bucketNum: b -= 1
#             }
#             LinkedList<Pair<?, Double>> bData = buckets.get(b);
#             bData.add(d);
            buckets[b].append(d)
#         }

#         LinkedList<Bucket> bucketList = new LinkedList<Bucket>();
        bucketList = []
#         for (LinkedList<Pair<?, Double>> bData : buckets) {
        for bData in buckets:
#             bucketList.add(new Bucket(bData));
            bucketList.append(Bucket(bData))
#         }

#         return bucketList;
        return bucketList
#     }
# }
