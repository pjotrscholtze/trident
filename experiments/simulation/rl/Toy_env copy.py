""" 
The environment simulates the possibility of buying or selling a good. The agent can either have one unit or zero unit of that good. At each transaction with the market, the agent obtains a reward equivalent to the price of the good when selling it and the opposite when buying. In addition, a penalty of 0.5 (negative reward) is added for each transaction.
Two actions are possible for the agent:
- Action 0 corresponds to selling if the agent possesses one unit or idle if the agent possesses zero unit.
- Action 1 corresponds to buying if the agent possesses zero unit or idle if the agent already possesses one unit.
The state of the agent is made up of an history of two punctual observations:
- The price signal
- Either the agent possesses the good or not (1 or 0)
The price signal is build following the same rules for the training and the validation environment. That allows the agent to learn a strategy that exploits this successfully.

"""

import numpy as np
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

from deer.base_classes import Environment
import json

ACTION_TO_TEXT = {
    0: "REMOVE_FROM_CACHE",
    1: "NO_CHANGE",
    2: "ADD_TO_CACHE"
}
ACTION_REMOVE_FROM_CACHE = 0
ACTION_NO_CHANGE = 1
ACTION_ADD_TO_CACHE = 2

def load_data():
    with open("/storage/wdps/trident/experiments/results/query_sets/25000_10.json") as f:
        tmp = json.load(f)
        return tmp[:128]
    

class MyEnv(Environment):
    
    def __init__(self, rng):
        """ Initialize environment.

        Parameters
        -----------
        rng : the numpy random number generator
        """
        self._raw_data = load_data()

        # Defining the type of environment
        self._last_ponctual_observation = [0, 0] # At each time step, the observation is made up of two elements, each scalar
        
        self._random_state = rng
                
        # Building a price signal with some patterns
        _price_signal=[]
        for sample in self._raw_data:
            _price_signal.append(sample["q"]["totalexec"])
        #     a=1
        #     pass
        # for i in range (1000):
        #     price = np.array([0.,0.,0.,-1.,0.,1.,0., 0., 0.])
        #     price += self._random_state.uniform(0, 3)
        #     _price_signal.extend(price.tolist())
        self._cache = {}
        self._cache_size = 0
        self._cache_size_limit = 10
       
        self._signal_train = _price_signal[:len(_price_signal)//2]
        self._signal_valid = _price_signal[len(_price_signal)//2:]
        # self._prices = None
        self._counter = 1
        self._offset = 0
                
    def reset(self, mode):
        """ Resets the environment for a new episode.

        Parameters
        -----------
        mode : int
            -1 is for the training phase, others are for validation/test.

        Returns
        -------
        list
            Initialization of the sequence of observations used for the pseudo-state; dimension must match self.inputDimensions().
            If only the current observation is used as a (pseudo-)state, then this list is equal to self._last_ponctual_observation.
        """
        if mode == -1:
            self.current_signal = self._signal_train
            self._offset = 0
        else:
            self.current_signal = self._signal_valid
            self._offset = len(self._signal_train)
        
        self._last_ponctual_observation = [self.current_signal[0], 0]

        self._counter = 1
        return [6*[0], 0]


    def _del_from_cache(self, idx, s, p, o):
        if idx not in self._cache or s not in self._cache[idx] or \
            p not in self._cache[idx][s] or o not in self._cache[idx][s][p]:
            return
        self._cache[idx][s][p].remove(o)
        self._cache_size -= 1

    def _add_to_cache(self, idx, s, p, o):
        if self._cache_size >= self._cache_size_limit: return
        if idx not in self._cache:
            self._cache[idx] = {}
        if s not in self._cache[idx]:
            self._cache[idx][s] = {}
        if p not in self._cache[idx][s]:
            self._cache[idx][s][p] = set()
        self._cache[idx][s][p].add(o)
        self._cache_size += 1
    
    def _get_duration(self, q):
        cached_time = 0

        for m in q["measurements"]:
            cached_time += m['duration']

        return q["totalexec"] - cached_time
    

    def act(self, action):
        """ Performs one time-step within the environment and updates the current observation self._last_ponctual_observation

        Parameters
        -----------
        action : int
            Integer in [0, ..., N_A] where N_A is the number of actions given by self.nActions()

        Returns
        -------
        reward: float
        """
        reward = 0
        
        # if (action == 0 and self._last_ponctual_observation[1] == 1):
        #     reward = self.current_signal[self._counter-1] - 0.5
        # if (action == 1 and self._last_ponctual_observation[1] == 0):
        #     reward = -self.current_signal[self._counter-1] - 0.5
        
        query = self._raw_data[self._offset + self._counter]["q"]

        handler = lambda idx, s, p, o: 1
        if action == ACTION_ADD_TO_CACHE:
            handler = self._add_to_cache
        elif action == ACTION_REMOVE_FROM_CACHE:
            handler = self._del_from_cache

        print("action", ACTION_TO_TEXT[action], "cache_size", self._cache_size, "original_time",self.current_signal[self._counter], "improved", self.current_signal[self._counter] - self._get_duration(query))
        for m in query["measurements"]:
            handler(m["idx"], m["s"], m["p"], m["o"])
        # time = self._get_duration(query)

        self._last_ponctual_observation[0] = self.current_signal[self._counter]
        self._last_ponctual_observation[1] = action

        self._counter += 1
        
        return -self._get_duration(query)

    def summarizePerformance(self, test_data_set, *args, **kwargs):
        """
        This function is called at every PERIOD_BTW_SUMMARY_PERFS.
        Parameters
        -----------
            test_data_set
        """
    
        print ("Summary Perf")
        
        observations = test_data_set.observations()
        duration = observations[0]
        action = observations[1]
        o_duration = observations[0][100:200]
        o_action = observations[1][100:200]
        
        steps=np.arange(len(duration))
        steps_long=np.arange(len(duration)*10)/10.
        
        #print steps,action,duration
        host = host_subplot(111, axes_class=AA.Axes)
        plt.subplots_adjust(right=0.9, left=0.1)
    
        par1 = host.twinx()
    
        host.set_xlabel("Time")
        host.set_ylabel("duration")
        par1.set_ylabel("action")
    
        p1, = host.plot(steps_long, np.repeat(duration,10), lw=3, c = 'b', alpha=0.8, ls='-', label = 'duration')
        p2, = par1.plot(steps, action, marker='o', lw=3, c = 'g', alpha=0.5, ls='-', label = 'action')
    
        par1.set_ylim(-0.09, 1.09)
    
    
        host.axis["left"].label.set_color(p1.get_color())
        par1.axis["right"].label.set_color(p2.get_color())
    
        plt.savefig("plot.png")
        print ("A plot of the policy obtained has been saved under the name plot.png")
    
    def inputDimensions(self):
        return [(6,), (1,)]     # We consider an observation made up of an history of 
                                # - the last six for the first scalar element obtained
                                # - the last one for the second scalar element


    def nActions(self):
        return 3                # The environment allows two different actions to be taken at each time step


    def inTerminalState(self):
        return False

    def observe(self):
        return np.array(self._last_ponctual_observation)

                


def main():
    # Can be used for debug purposes
    rng = np.random.RandomState(123456)
    myenv = MyEnv(rng)

    print (myenv.observe())
    
if __name__ == "__main__":
    main()
