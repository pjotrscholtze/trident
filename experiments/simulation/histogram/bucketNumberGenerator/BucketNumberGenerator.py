# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.histogram.bucketNumberGenerator;

# /**
#  * @author herald
#  */
# public interface BucketNumberGenerator {
class BucketNumberGenerator:
#     boolean hasNext();
    def hasNext(self) -> bool: raise NotImplementedError()

#     int getNext();
    def getNext(self) -> int: raise NotImplementedError()
# }
