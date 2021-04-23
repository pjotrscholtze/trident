# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */

# /**
#  * @author herald
#  */
class BucketNumberGenerator:
    def has_next(self) -> bool: raise NotImplementedError()

    def get_next(self) -> int: raise NotImplementedError()
