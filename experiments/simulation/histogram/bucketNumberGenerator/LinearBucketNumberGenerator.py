# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from bucketNumberGenerator.BucketNumberGenerator import BucketNumberGenerator

# /**
#  * @author Herald Kllapi <br>
#  *         University of Athens /
#  *         Department of Informatics and Telecommunications.
#  * @since 1.0
#  */
class LinearBucketNumberGenerator(BucketNumberGenerator):

    def __init__(self, start: int, step: int, max: int):
        self.step = step
        self.max = max
        self.current = start

    def has_next(self) -> bool: return self.current <= self.max

    def get_next(self) -> int:
        ret: int = self.current
        self.current += self.step
        return ret
