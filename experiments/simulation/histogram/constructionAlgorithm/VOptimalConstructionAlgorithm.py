# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from typing import List
# package madgik.exareme.utils.histogram.constructionAlgorithm;
from constructionAlgorithm.ConstructionAlgorithm import ConstructionAlgorithm


# import madgik.exareme.utils.association.Pair;
# import madgik.exareme.utils.histogram.Bucket;
from Bucket import Bucket
# import madgik.exareme.utils.histogram.constructionAlgorithm.vOptimalSA.VOptimalSA;
from constructionAlgorithm.vOptimalSA.VOptimalSA import VOptimalSA
# import madgik.exareme.utils.histogram.constructionAlgorithm.vOptimalSA.VOptimalState;
from constructionAlgorithm.vOptimalSA.VOptimalState import VOptimalState
# import madgik.exareme.utils.histogram.partitionRule.PartitionRule;
from partitionRule.PartitionRule import PartitionRule
# import madgik.exareme.utils.simulatedAnnealing.LogarithmicTemperature;
from simulatedAnnealing.LogarithmicTemperature import LogarithmicTemperature

# import java.rmi.AccessException;
# import java.rmi.RemoteException;
# import java.util.ArrayList;
# import java.util.LinkedList;

# /**
#  * @author herald
#  */
# public class VOptimalConstructionAlgorithm implements ConstructionAlgorithm {
class VOptimalConstructionAlgorithm(ConstructionAlgorithm):
#     private static final long serialVersionUID = 1L;

#     public LinkedList<Bucket> createHistogram(ArrayList<Pair<?, Double>> data, int bucketNum,
    def createHistogram(self, data: List[tuple[any,float]], bucketNum: int,
        partitionRule: PartitionRule) -> List[Bucket]:

#         if (bucketNum < 1) {
#             throw new AccessException("Bucket num should be > 0");
#         }
        if bucketNum < 1: raise AttributeError("Bucket num should be > 0")

#         LinkedList<Bucket> bucketList = new LinkedList<Bucket>();
        bucketList:List[Bucket] = []

#         // Put everything into 1 bucket.
#         if (bucketNum == 1) {
        if bucketNum == 1:
#             Bucket b = new Bucket(data);
#             bucketList.add(b);

#             return bucketList;
            return [Bucket(data)]
#         }

#         VOptimalSA sa =
#             new VOptimalSA(10000, 1000, new LogarithmicTemperature(1.0), data, bucketNum);
        sa = VOptimalSA(10000, 1000, LogarithmicTemperature(1.0), data, bucketNum)

#         VOptimalState result = (VOptimalState) sa.search();
        result: VOptimalState = sa.search()

#         int index = 0;
        index:int = 0
#         for (int t : result.thresholds) {
        for t in result.thresholds:
#             Bucket b = new Bucket(data.subList(index, t));
            b = Bucket(data[index: t])
            bucketList.append(b)
#             bucketList.add(b);

#             index = t;
            index = t
#         }

#         Bucket b = new Bucket(data.subList(index, data.size()));
        b:Bucket = Bucket(data[index:len(data)])
#         bucketList.add(b);
        bucketList.append(b)

#         return bucketList;
        return bucketList
#     }
# }
