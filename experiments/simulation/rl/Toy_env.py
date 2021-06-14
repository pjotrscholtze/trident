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

def load_table_sizes(path):
    path = "/storage/wdps/trident/experiments/get_tablesizes/results.json"
    # /storage/wdps/trident/experiments/get_tablesizes/results.json
    with open(path) as f:
        return json.load(f)

def load_data(path):
    # "/storage/wdps/trident/experiments/results/query_sets/25000_10.json"
    with open(path) as f:
        return json.load(f)
        # tmp = json.load(f)
        # t = tmp[:512]
        # np.random.shuffle(t)
        # return t

class Observation:
    @staticmethod
    def blank():
        return Observation(*([0]* (Observation.__init__.__code__.co_argcount -1)))
    def __init__(self, table_generation_time, action, no_measurements, cache_size,
            in_cache, idx, query_duration, queries_per_second, cache_usage_ratio,
            query_optimization_time, table_size, spo_touch, ops_touch,
            pos_touch, sop_touch, osp_touch, pso_touch, n_resulting_rows,
            finished, stats_row, stats_column, stats_cluster, aggr_indices,
            not_aggr_indices, cache_indices):
        self.table_generation_time = table_generation_time
        self.action = action
        self.no_measurements = no_measurements
        self.cache_size = cache_size
        self.in_cache = in_cache
        self.idx = idx
        self.query_duration = query_duration
        self.queries_per_second = queries_per_second
        self.cache_usage_ratio = cache_usage_ratio
        self.query_optimization_time = query_optimization_time
        self.table_size = table_size
        self.spo_touch = spo_touch
        self.ops_touch = ops_touch
        self.pos_touch = pos_touch
        self.sop_touch = sop_touch
        self.osp_touch = osp_touch
        self.pso_touch = pso_touch
        self.n_resulting_rows = n_resulting_rows
        self.finished = finished
        self.stats_row = stats_row
        self.stats_column = stats_column
        self.stats_cluster = stats_cluster
        self.aggr_indices = aggr_indices
        self.not_aggr_indices = not_aggr_indices
        self.cache_indices = cache_indices

        # self._last_ponctual_observation[0] = self.current_signal[self._counter]
        # self._last_ponctual_observation[1] = action
        # self._last_ponctual_observation[2] = len(query["measurements"])
        # self._last_ponctual_observation[3] = self._cache_size
        # self._last_ponctual_observation[4] = self._is_in_cache(m["idx"], m["s"], m["p"], m["o"])
        # self._last_ponctual_observation[5] = m["idx"]
    def to_list(self):
        res = []
        for k in sorted(self.__dict__.keys()):
            res.append(self.__getattribute__(k))
        return res
        

# print(Observation.__init__.__code__.co_argcount)
class Settings:

    @staticmethod
    def count_observation_features() -> int:
        return Observation.__init__.__code__.co_argcount - 1

    @staticmethod
    def generate_settings(data_path: str, cache_size_limit: int, mask_nr: int, history_size: int):
        if mask_nr >= 2**Settings.count_observation_features() or mask_nr < 0:
            raise ValueError
        pass

        tmp = mask_nr
        args = []
        for i in range(0, Settings.count_observation_features()):
            args.append(tmp % 2)
            tmp = int(tmp / 2)
        
        return Settings(data_path, cache_size_limit, Observation(*args), history_size)

    def to_dict(self):
        res = self.__dict__
        res["observation_mask"] = self.observation_mask.__dict__
        return res

    def __init__(self, data_path: str, cache_size_limit: int, observation_mask: Observation, history_size: int):
        self.data_path = data_path
        self.cache_size_limit = cache_size_limit
        self.observation_mask = observation_mask
        self.history_size = history_size

    def apply_observation_mask(self, observation: Observation):
        for key in observation.__dict__:
            observation.__setattr__(key, self.observation_mask.__getattribute__(key) * observation.__getattribute__(key))
        return observation

class MyEnv(Environment):
    def _new_last_ponctual_observation(self):
        return Observation.blank().to_list() #[0, 0, 0, 0, 0]
    # def _new_last_ponctual_observation(self): return [0, 0, 0, 0, 0, 0]

    def __init__(self, rng, settings = None):
        """ Initialize environment.

        Parameters
        -----------
        rng : the numpy random number generator
        """
        print("init")
        if settings is None:
            settings = Settings.generate_settings("/storage/wdps/trident/experiments/results/query_sets/25000_10.json", 2000, 2**Settings.count_observation_features() - 1, 1)
        self.settings = settings
        self._raw_data = []
        self._raw_data_m = []

        # self._table_sizes = load_table_sizes("/storage/wdps/trident/experiments/get_tablesizes/results.json")
        self._table_sizes = load_table_sizes("/var/scratch/pse740/cache/table_size.json")
        # /storage/wdps/trident/experiments/get_tablesizes/results.json


        # Defining the type of environment
        self._last_ponctual_observation = self._new_last_ponctual_observation() # At each time step, the observation is made up of two elements, each scalar
        
        self._random_state = rng
                
        # Building a price signal with some patterns
        _price_signal=[]
        for sample in load_data(self.settings.data_path):
            for m in sample["q"]["measurements"]:
                _price_signal.append(m["duration"])
                self._raw_data.append(sample)
                self._raw_data_m.append(m)

        print("total", len(self._raw_data))
        #     a=1
        #     pass
        # for i in range (1000):
        #     price = np.array([0.,0.,0.,-1.,0.,1.,0., 0., 0.])
        #     price += self._random_state.uniform(0, 3)
        #     _price_signal.extend(price.tolist())
        self._cache = {}
        self._cache_size = 0
        self._cache_size_limit = self.settings.cache_size_limit
       
        self._signal_train = _price_signal[:len(_price_signal)//2]
        self._signal_valid = _price_signal[len(_price_signal)//2:]
        # self._prices = None
        self._counter = 1
        self._offset = 0
        self._exec_time = [0]
        self._exec_time_before = [0]
        self._cached_tables_count = [0]
        self._avg_queries_per_second = None
                
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
        print("reset", mode)
        print("_cache_size", self._cache_size)
        print("self._cached_tables_count", self._cached_tables_count[len(self._cached_tables_count)-1])
        print("self._cache",self._cache)
        ratio = "inf"
        if sum(self._exec_time) >0:
            ratio = sum(self._exec_time) / sum(self._exec_time_before)
        print("perf diff", ratio,  sum(self._exec_time_before), sum(self._exec_time))
        self._cache = {}
        if mode == -1:
            self.current_signal = self._signal_train
            self._offset = 0
        else:
            self.current_signal = self._signal_valid
            self._offset = len(self._signal_train)
        
        self._last_ponctual_observation = self._new_last_ponctual_observation()#
        self._last_ponctual_observation[0] = self.current_signal[0]
        self._avg_queries_per_second = None
        # [self.current_signal[0], 0, 0]

        self._counter = 1
        self._exec_time_before = [0]
        self._exec_time = [0]
        self._cached_tables_count = [0]
        self._cache_size = 0

        base = []
        for i in Observation.blank().to_list():
            base.append(6*[0])
        
        return base
        # return [6*[0], 6*[0], 6*[0], 6*[0], 6*[0]]

    def get_table_size(self, s, p, o):
        return self._table_sizes[str(s)][str(p)][str(o)]

    def _del_from_cache(self, idx, s, p, o):
        if idx not in self._cache or s not in self._cache[idx] or \
            p not in self._cache[idx][s] or o not in self._cache[idx][s][p]:
            return
        self._cache_size -= self.get_table_size(s, p, o)
        self._cache[idx][s][p].remove(o)

    def _add_to_cache(self, idx, s, p, o):
        if self._cache_size >= self._cache_size_limit: return
        if idx not in self._cache:
            self._cache[idx] = {}
        if s not in self._cache[idx]:
            self._cache[idx][s] = {}
        if p not in self._cache[idx][s]:
            self._cache[idx][s][p] = []
        self._cache[idx][s][p].append(o)
        # self._cache_size += 1
        self._cache_size += self.get_table_size(s, p, o)

    def _is_in_cache(self, idx, s, p, o):
        if idx not in self._cache:
            return False
        if s not in self._cache[idx]:
            return False
        if p not in self._cache[idx][s]:
            return False
        return o in self._cache[idx][s][p]

    def _get_duration(self, q):
        cached_time = 0

        for m in q["measurements"]:
            if self._is_in_cache(m["idx"], m["s"], m["p"], m["o"]):
                cached_time += m['duration']

        return max(0, q["totalexec"] - cached_time)
    

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

        self._exec_time.append(self._exec_time[len(self._exec_time)-1] + self._get_duration(query))
        self._exec_time_before.append(self._exec_time_before[len(self._exec_time_before)-1] + query["totalexec"])
        self._cached_tables_count.append(self._cache_size)

        # print("action", ACTION_TO_TEXT[action], "cache_size", self._cache_size, "original_time",self.current_signal[self._counter], "improved", query["totalexec"] - self._get_duration(query))
        m = self._raw_data_m[self._counter]
        # for m in query["measurements"]:
        # time = self._get_duration(query)
        obs = Observation.blank()

        obs.table_generation_time = self.current_signal[self._counter]
        obs.action = action
        obs.no_measurements = len(query["measurements"])
        obs.cache_size = self._cache_size
        obs.in_cache = self._is_in_cache(m["idx"], m["s"], m["p"], m["o"])
        obs.idx = m["idx"]
        obs.table_size = self.get_table_size(m["s"], m["p"], m["o"])

        obs.query_duration = query['totalexec']
        obs.query_optimization_time = query['queryopti']
        obs.spo_touch = query["spo"]
        obs.ops_touch = query["ops"]
        obs.pos_touch = query["pos"]
        obs.sop_touch = query["sop"]
        obs.osp_touch = query["osp"]
        obs.pso_touch = query["pso"]

        obs.n_resulting_rows = query['nResultingRows']
        obs.finished = query["finished"]
        obs.stats_row = query["statsRow"]
        obs.stats_column = query["statsColumn"]
        obs.stats_cluster = query["statsCluster"]
        obs.aggr_indices = query["aggrIndices"]
        obs.not_aggr_indices = query["notAggrIndices"]
        obs.cache_indices = query["cacheIndices"]



        # obs.queries_per_second
        obs.cache_usage_ratio = self._cache_size / self._cache_size_limit

        # self._last_ponctual_observation[0] = self.current_signal[self._counter]
        # self._last_ponctual_observation[1] = action
        # self._last_ponctual_observation[2] = len(query["measurements"])
        # self._last_ponctual_observation[3] = self._cache_size
        # self._last_ponctual_observation[4] = self._is_in_cache(m["idx"], m["s"], m["p"], m["o"])
        # self._last_ponctual_observation[5] = m["idx"]

        # With action: perf diff 0.14046897492989455

        self._counter += 1
        before = self._get_duration(query)
        handler(m["idx"], m["s"], m["p"], m["o"])

    
        # ratio = 0
        # if sum(self._exec_time) >0:
        #     ratio = sum(self._exec_time) / sum(self._exec_time_before)

        _duration = self._get_duration(query)
        proto_query_per_second = 1
        if self._avg_queries_per_second is not None:
            proto_query_per_second +=  self._avg_queries_per_second

        if _duration > 0:
            proto_query_per_second = 1 / self._get_duration(query)

        if self._avg_queries_per_second is None:
            self._avg_queries_per_second = proto_query_per_second
        self._avg_queries_per_second = (self._avg_queries_per_second * 0.9) + (proto_query_per_second * 0.1)
        obs.queries_per_second = self._avg_queries_per_second


        list_obs = self.settings.apply_observation_mask(obs).to_list()
        for k,_ in enumerate(self._last_ponctual_observation):
            self._last_ponctual_observation[k] = list_obs[k]

        return before - self._get_duration(query) #-self._get_duration(query)

    def summarizePerformance(self, test_data_set, *args, **kwargs):
        """
        This function is called at every PERIOD_BTW_SUMMARY_PERFS.
        Parameters
        -----------
            test_data_set
        """
        # observations = test_data_set.observations()
        # def np_arr_to_list(nparr):
        #     res = []
        #     for v in nparr:
        #         if isinstance(v, np.ndarray):
        #             v = np_arr_to_list(v)
        #         else: v = float(v)
        #         res.append(v)
        #     return res

        # w = np_arr_to_list(list(args[0].q_vals.get_weights()))
        # for v in list(args[0].q_vals.get_weights()):
        #     w2 = []
        #     for v2 in list(v):
        #         if isinstance(v2, np.ndarray):
        #             w3 = []
        #             for v3 in v2:
        #                 try:
        #                     w3.append(float(v3))
        #                 except Exception as e:
        #                     print(v3)
        #                     raise e
        #             w2.append(w3)

        #         else:
        #             w2.append(float(v2))
        #     w.append(w2)
        results = {
            "settings": self.settings.to_dict(),
            "cache": self._cache,
            "counter": self._counter,
            "exec_time_before": self._exec_time_before,
            "exec_time": self._exec_time,
            "cached_tables_count": self._cached_tables_count,
            "cache_size": self._cache_size,

            # "q_vals": w,
            # "input_dimensions": args[0]._input_dimensions,
            # "n_actions": args[0]._n_actions,

            # "duration": [float(o) for o in observations[0]],
            # "action": [float(o) for o in observations[1]],


        }
        print("### RESULTS ###", json.dumps(results), flush=True)
        print("---")
        # args[0].q_vals
        # args[0]._input_dimensions
        # args[0]._n_actions

        # duration = list(observations[0])
        # action = list(observations[1])

        # kwargs['train_data_set'].n_elems

        # print ("Summary Perf")
        # print(self._cached_tables_count)

        # print(self._cache)
        # print("perf diff", sum(self._exec_time_before) / sum(self._exec_time),  sum(self._exec_time_before), sum(self._exec_time))


        # plt.title("time v cached_tables_count")
        # plt.plot(range(0, len(self._cached_tables_count)), self._cached_tables_count, label = "cached_tables_count")
        # plt.legend()
        # plt.show()

        
        # # plot lines
        # plt.title("time performance difference")
        # plt.plot(range(0, len(self._exec_time_before)), self._exec_time, label = "exec_time")
        # plt.plot(range(0, len(self._exec_time_before)), self._exec_time_before, label = "exec_time_before")
        # plt.legend()
        # plt.show()

        

        # plt.title("time log(performance difference)")
        # plt.plot(range(0, len(self._exec_time_before)), np.log(self._exec_time), label = "exec_time")
        # plt.plot(range(0, len(self._exec_time_before)), np.log(self._exec_time_before), label = "exec_time_before")
        # plt.legend()
        # plt.show()
        

        a=1
        # observations = test_data_set.observations()
        # duration = observations[0]
        # action = observations[1]

        # duration = self._exec_time
        # before = self._exec_time_before
        # o_duration = observations[0][100:200]
        # o_action = observations[1][100:200]
        
        # steps=np.arange(len(duration))
        # steps_long=np.arange(len(duration)*10)/10.
        
        # #print steps,before,duration
        # host = host_subplot(111, axes_class=AA.Axes)
        # # plt.subplots_adjust(right=0.9, left=0.1)
    
        # par1 = host.twinx()
    
        # host.set_xlabel("time--")
        # host.set_ylabel("i")
        # par1.set_ylabel("before")
    
        # p1, = host.plot(steps, duration, lw=3, c = 'b', alpha=0.8, ls='-', label = 'duration')
        # # p1, = host.plot(steps_long, np.repeat(duration,10), lw=3, c = 'b', alpha=0.8, ls='-', label = 'duration')
        # p2, = par1.plot(steps, before, marker='o', lw=3, c = 'g', alpha=0.5, ls='-', label = 'action')
    
        # # par1.set_ylim(-0.09, 1.09)
    
    
        # host.axis["left"].label.set_color(p1.get_color())
        # par1.axis["right"].label.set_color(p2.get_color())
    
        # plt.savefig("plot.png")
        # print ("A plot of the policy obtained has been saved under the name plot.png")
    
    def inputDimensions(self):
        base = []
        for i in Observation.blank().to_list():
            base.append((self.settings.history_size,))
        
        return base

        # return [(6,), (6,), (6,), (6,), (6,)]     # We consider an observation made up of an history of 
        # return [(6,), (1,), (1,), (1,), (1,), (1,)]     # We consider an observation made up of an history of 
                                # - the last six for the first scalar element obtained
                                # - the 2th one for the second scalar element
                                # - the 3th one for the number of measurements
                                # - the 4th one for the number of items in cache
                                # - the last one for if the item is in the cache


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
