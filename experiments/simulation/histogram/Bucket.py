# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from typing import List

# /**
#  * @author herald
#  */
class Bucket:

    def __init__(self, data: List): self.data = data
    # def __init__(self, data: List[tuple[any, float]]): self.data = data

    def clone(self): return Bucket([] + self.data)
