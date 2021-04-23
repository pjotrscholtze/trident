from partitionRule.PartitionClass import PartitionClass
from partitionRule.PartitionConstraint import PartitionConstraint

# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.histogram.partitionRule;

# /**
#  * @author herald
#  */
# public class PartitionRule {
class PartitionRule:
    def __init__(self, partitionClass: PartitionClass, partitionConstraint: PartitionConstraint):
        self.partitionClass = partitionClass
        self.partitionConstraint = partitionConstraint
#     public PartitionClass partitionClass = null;
#     public PartitionConstraint partitionConstraint = null;

#     public PartitionRule(PartitionClass partitionClass, PartitionConstraint partitionConstraint) {
#         this.partitionClass = partitionClass;
#         this.partitionConstraint = partitionConstraint;
#     }
# }
