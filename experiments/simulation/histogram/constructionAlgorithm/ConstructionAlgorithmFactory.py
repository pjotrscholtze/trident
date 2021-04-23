# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.histogram.constructionAlgorithm;
from constructionAlgorithm.ConstructionAlgorithm import ConstructionAlgorithm
# import madgik.exareme.utils.histogram.partitionRule.PartitionConstraint;
from partitionRule.PartitionConstraint import PartitionConstraint
# import madgik.exareme.utils.histogram.partitionRule.PartitionRule;
from partitionRule.PartitionRule import PartitionRule
from constructionAlgorithm.MaxDiffConstructionAlgorithm import MaxDiffConstructionAlgorithm
from constructionAlgorithm.VOptimalConstructionAlgorithm import VOptimalConstructionAlgorithm
from constructionAlgorithm.EquiWidthConstructionAlgorithm import EquiWidthConstructionAlgorithm

# /**
#  * @author herald
#  */
# public class ConstructionAlgorithmFactory {
class ConstructionAlgorithmFactory:
    def __init__(self): raise Exception("No constructor for this class!")
#     private ConstructionAlgorithmFactory() {
#     }
    @staticmethod
    def getAlgorithm(partitionRule: PartitionRule) -> ConstructionAlgorithm:
        if (partitionRule.partitionConstraint == PartitionConstraint.maxdiff):
            return MaxDiffConstructionAlgorithm()

        if (partitionRule.partitionConstraint == PartitionConstraint.v_optimal):
            return VOptimalConstructionAlgorithm()

        if (partitionRule.partitionConstraint == PartitionConstraint.equi_width):
            return EquiWidthConstructionAlgorithm()

        raise NotImplementedError("Not supported yet!")

#     public static ConstructionAlgorithm getAlgorithm(PartitionRule partitionRule) {
#         if (partitionRule.partitionConstraint == PartitionConstraint.maxdiff) {
#             return new MaxDiffConstructionAlgorithm();
#         }

#         if (partitionRule.partitionConstraint == PartitionConstraint.v_optimal) {
#             return new VOptimalConstructionAlgorithm();
#         }

#         if (partitionRule.partitionConstraint == PartitionConstraint.equi_width) {
#             return new EquiWidthConstructionAlgorithm();
#         }

#         throw new UnsupportedOperationException("Not supported yet!");
#     }
# }
