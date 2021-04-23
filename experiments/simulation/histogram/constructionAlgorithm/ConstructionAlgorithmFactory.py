# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from constructionAlgorithm.ConstructionAlgorithm import ConstructionAlgorithm
from partitionRule.PartitionConstraint import PartitionConstraint
from partitionRule.PartitionRule import PartitionRule
from constructionAlgorithm.MaxDiffConstructionAlgorithm import MaxDiffConstructionAlgorithm
from constructionAlgorithm.VOptimalConstructionAlgorithm import VOptimalConstructionAlgorithm
from constructionAlgorithm.EquiWidthConstructionAlgorithm import EquiWidthConstructionAlgorithm


ALGOS = {
    PartitionConstraint.maxdiff.value: MaxDiffConstructionAlgorithm,
    PartitionConstraint.v_optimal.value: VOptimalConstructionAlgorithm,
    PartitionConstraint.equi_width.value: EquiWidthConstructionAlgorithm
}

# /**
#  * @author herald
#  */
class ConstructionAlgorithmFactory:
    def __init__(self): raise Exception("No constructor for this class!")

    @staticmethod
    def get_algorithm(partitionRule: PartitionRule) -> ConstructionAlgorithm:
        if partitionRule.partitionConstraint.value not in ALGOS:
            raise NotImplementedError("Not supported yet!")
        return ALGOS[partitionRule.partitionConstraint.value]()


