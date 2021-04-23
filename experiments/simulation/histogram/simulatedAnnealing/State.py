# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */

# /**
#  * @author herald
#  */
class State:

    def clone(self) -> any: raise NotImplementedError()

    def getCost(self) -> float: raise NotImplementedError()
