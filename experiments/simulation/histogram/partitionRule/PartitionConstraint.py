from enum import Enum
# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.histogram.partitionRule;


# /**
#  * This is a mathematical constraint on the source
#  * parameter that uniquely identifies a single histogram
#  * within its partition class. Several partition constraints
#  * have been proposed so far, e.g., equi-sum, v-optimal, maxdiff,
#  * and compressed, which are defined further below as they are
#  * introduced. Many of the more successful ones try to avoid
#  * grouping vastly different source parameter values into a bucket.
#  * <p/>
#  * [The History of Histograms Yannis Ioannidis]
#  *
#  * @author herald
#  */
# public enum PartitionConstraint {
class PartitionConstraint(Enum):
    equi_width = "equi_width",
    equi_height = "equi_height",
    equi_sum = "equi_sum",
    v_optimal = "v_optimal",
    maxdiff = "maxdiff",
    compressed = "compressed"

#     equi_width,
#     equi_height,
#     equi_sum,
#     v_optimal,
#     maxdiff,
#     compressed
# }
