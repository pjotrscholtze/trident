# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.histogram.bucketNumberGenerator;
from bucketNumberGenerator.BucketNumberGenerator import BucketNumberGenerator

# /**
#  * @author Herald Kllapi <br>
#  *         University of Athens /
#  *         Department of Informatics and Telecommunications.
#  * @since 1.0
#  */
# public class LinearBucketNumberGenerator implements BucketNumberGenerator {
class LinearBucketNumberGenerator(BucketNumberGenerator):

#     private int step = 0;
#     private int max = 0;
#     private int current = 0;

    def __init__(self, start: int, step: int, max: int):
#     public LinearBucketNumberGenerator(int start, int step, int max) {
#         this.step = step;
        self.step = step
#         this.max = max;
        self.max = max

#         this.current = start;
        self.current = start
#     }

#     public boolean hasNext() {
    def hasNext(self) -> bool:
        return self.current <= self.max
#         return current <= max;

#     }

#     public int getNext() {
    def getNext(self) -> int:
#         int ret = current;
        ret:int = self.current
#         current += step;
        self.current += self.step
#         return ret;
        return ret
#     }
# }
