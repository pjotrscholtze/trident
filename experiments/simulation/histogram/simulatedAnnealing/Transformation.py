# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.simulatedAnnealing;
from simulatedAnnealing.State import State
# import java.io.Serializable;
# import java.rmi.RemoteException;

# /**
#  * @author herald
#  */
# public interface Transformation extends Serializable {
class Transformation:

#     State apply(State state) throws RemoteException;
    def apply(self, state: State) -> State: raise NotImplementedError()
# }
