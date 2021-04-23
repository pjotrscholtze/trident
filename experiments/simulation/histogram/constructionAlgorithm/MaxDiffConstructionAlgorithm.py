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
# import java.util.*;
from queue import PriorityQueue
from typing import List
# /**
#  * @author herald
#  */
# public class MaxDiffConstructionAlgorithm implements ConstructionAlgorithm {
class MaxDiffConstructionAlgorithm(ConstructionAlgorithm):
    pass

#     private static final long serialVersionUID = 1L;

#     public LinkedList<Bucket> createHistogram(ArrayList<Pair<?, Double>> data, int bucketNum,
#         PartitionRule partitionRule) throws RemoteException {
    def createHistogram(self, data: List[tuple[any,float]], bucketNum: int,
        partitionRule: PartitionRule) -> List[Bucket]:

#         PriorityQueue<Pair<Double, Integer>> diffQueue =
#             new PriorityQueue<Pair<Double, Integer>>(bucketNum,
#                 new Comparator<Pair<Double, Integer>>() {

#                     public int compare(Pair<Double, Integer> o1, Pair<Double, Integer> o2) {
#                         return o1.a.compareTo(o2.a);
#                     }
#                 });
        diff_queue = PriorityQueue()

#         for (int i = 0; i < data.size() - 1; i++) {
        for i in range(0, len(data) - 1):
#             Pair<?, Double> d1 = data.get(i);
            d1 = data[i]
#             Pair<?, Double> d2 = data.get(i + 1);
            d2 = data[i]

#             diffQueue.offer(new Pair<Double, Integer>(d2.b - d1.b, i + 1));
            diff_queue.put((d2[1] - d1[1], i + 1))

#       /* Remove the first */
#             if (i >= bucketNum - 1) {
            if (i >= bucketNum - 1):
#                 diffQueue.poll();
                diff_queue.get()
#             }
#         }

#         //	for(Triple<Double, Integer, Integer> t : diffQueue) {
#         //	    log.debug(">> " + t.a);
#         //	}

#         LinkedList<Bucket> bucketList = new LinkedList<Bucket>();
        bucket_list: List[Bucket] = []

#     /* Sort the buckets */
#         ArrayList<Pair<Double, Integer>> thresholdArray =
#             new ArrayList<Pair<Double, Integer>>(diffQueue);
        thresholdArray = []
        while not diff_queue.empty(): thresholdArray.append(diff_queue.get())
#         Collections.sort(thresholdArray, new Comparator<Pair<Double, Integer>>() {

#             public int compare(Pair<Double, Integer> o1, Pair<Double, Integer> o2) {
#                 return o1.b.compareTo(o2.b);
#             }
#         });
        def sorter(o): return o[1]
        thresholdArray.sort(key=sorter)

#         int index = 0;
        index:int = 0
#         for (Pair<Double, Integer> t : thresholdArray) {
        for t in thresholdArray:
#             Bucket b = new Bucket(data.subList(index, t.b));
            b = Bucket(data[index:t[1]])
#             bucketList.add(b);
            bucket_list.append(b)

#             index = t.b;
            index = t[1]
#         }

#         Bucket b = new Bucket(data.subList(index, data.size()));
        b = Bucket(data[index:len(data)])
#         bucketList.add(b);
        bucket_list.append(b)

#         return bucketList;
        return bucket_list
#     }
# }
