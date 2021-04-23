# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from enum import Enum

# /**
#  * This indicates if there are any restrictions on the buckets. Of great importance is the serial
#  * class, which requires that buckets are non-overlapping with respect to some parameter (the
#  * next characteristic), and its subclass end-biased, which requires at most one non-singleton
#  * bucket. [The History of Histograms Yannis Ioannidis]
#  *
#  * @author herald
#  */
class PartitionClass(Enum):
    serial = "serial",
    end_biased = "end_biased"
