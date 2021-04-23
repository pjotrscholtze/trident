# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from constructionAlgorithm.ConstructionAlgorithm import ConstructionAlgorithm
from partitionRule.PartitionConstraint import PartitionConstraint
from partitionRule.PartitionRule import PartitionRule
from constructionAlgorithm.MaxDiffConstructionAlgorithm import MaxDiffConstructionAlgorithm
from constructionAlgorithm.VOptimalConstructionAlgorithm import VOptimalConstructionAlgorithm
from constructionAlgorithm.EquiWidthConstructionAlgorithm import EquiWidthConstructionAlgorithm

# /**
#  * @author herald
#  */
class ConstructionAlgorithmFactory:
    def __init__(self): raise Exception("No constructor for this class!")

    @staticmethod
    def get_algorithm(partitionRule: PartitionRule) -> ConstructionAlgorithm:
        if partitionRule.partitionConstraint == PartitionConstraint.maxdiff:
            return MaxDiffConstructionAlgorithm()

        if partitionRule.partitionConstraint == PartitionConstraint.v_optimal:
            return VOptimalConstructionAlgorithm()

        if partitionRule.partitionConstraint == PartitionConstraint.equi_width:
            return EquiWidthConstructionAlgorithm()

        raise NotImplementedError("Not supported yet!")

