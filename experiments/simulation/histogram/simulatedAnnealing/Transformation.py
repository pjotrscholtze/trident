# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from simulatedAnnealing.State import State

# /**
#  * @author herald
#  */
class Transformation:
    def apply(self, state: State) -> State: raise NotImplementedError()
