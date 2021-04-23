# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
# package madgik.exareme.utils.simulatedAnnealing;

# import java.io.Serializable;
# import java.rmi.RemoteException;

# /**
#  * @author herald
#  */
# public interface State extends Serializable, Cloneable {
class State:

#     State clone();
    def clone(self) -> any: raise NotImplementedError()

#     double getCost() throws RemoteException;
    def getCost(self) -> float: raise NotImplementedError()
# }
