from typing import List
from partitionRule.PartitionRule import PartitionRule
from Bucket import Bucket
# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.histogram.constructionAlgorithm;

# import madgik.exareme.utils.association.Pair;
# import madgik.exareme.utils.histogram.Bucket;
# import madgik.exareme.utils.histogram.partitionRule.PartitionRule;

# import java.io.Serializable;
# import java.rmi.RemoteException;
# import java.util.ArrayList;
# import java.util.LinkedList;

# /**
#  * Given a particular partition rule, this is the algorithm
#  * that constructs histograms that satisfy the rule. It
#  * is often the case that, for the same histogram class,
#  * there are several construction algorithms with different efficiency.
#  * [The History of Histograms Yannis Ioannidis]
#  *
#  * @author herald
#  */
# public interface ConstructionAlgorithm extends Serializable {

class ConstructionAlgorithm:
    def createHistogram(self, data: List[tuple[any, float]], bucketNum: int,
        partitionRule: PartitionRule) -> List[Bucket]:
        raise NotImplementedError
        #  pass# throws RemoteException;
#     LinkedList<Bucket> createHistogram(ArrayList<Pair<?, Double>> data, int bucketNum,
#         PartitionRule partitionRule) throws RemoteException;
# }
