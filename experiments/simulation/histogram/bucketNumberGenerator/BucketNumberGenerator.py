# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */

# /**
#  * @author herald
#  */
class BucketNumberGenerator:
    def hasNext(self) -> bool: raise NotImplementedError()

    def getNext(self) -> int: raise NotImplementedError()
