from partitionRule.PartitionClass import PartitionClass
from partitionRule.PartitionConstraint import PartitionConstraint

# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */

# /**
#  * @author herald
#  */
class PartitionRule:
    def __init__(self, partitionClass: PartitionClass, partitionConstraint: PartitionConstraint):
        self.partitionClass = partitionClass
        self.partitionConstraint = partitionConstraint

