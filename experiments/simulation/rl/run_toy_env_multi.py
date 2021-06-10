"""Toy environment launcher. See the docs for more details about this environment.

"""
import os
os.environ["SM_FRAMEWORK"] = "tf.keras"

import sys
import logging, json
import numpy as np

from deer.default_parser import process_args
from deer.agent import NeuralAgent
from deer.learning_algos.q_net_keras import MyQNetwork
from Toy_env import MyEnv as Toy_env, Settings, Observation, load_data
import deer.experiment.base_controllers as bc
from deer.policies import EpsilonGreedyPolicy

logging.basicConfig(level=logging.INFO)



class Defaults:
    # ----------------------
    # Experiment Parameters
    # ----------------------
    STEPS_PER_EPOCH = 89 #int(1345/2-1)
    EPOCHS = 20
    STEPS_PER_TEST = 89 #int(1345/2-1)
    PERIOD_BTW_SUMMARY_PERFS = 10

    # ----------------------
    # Environment Parameters
    # ----------------------
    FRAME_SKIP = 1

    # ----------------------
    # DQN Agent parameters:
    # ----------------------
    UPDATE_RULE = 'rmsprop'
    LEARNING_RATE = 0.005
    LEARNING_RATE_DECAY = 1.
    DISCOUNT = 0.9
    DISCOUNT_INC = 1.
    DISCOUNT_MAX = 0.99
    RMS_DECAY = 0.9
    RMS_EPSILON = 0.0001
    MOMENTUM = 0
    CLIP_NORM = 1.0
    EPSILON_START = 1.0
    EPSILON_MIN = .1
    EPSILON_DECAY = 10000
    UPDATE_FREQUENCY = 1
    REPLAY_MEMORY_SIZE = 1000000
    BATCH_SIZE = 32
    FREEZE_INTERVAL = 1000
    DETERMINISTIC = True


def start_experiment(settings):
    logging.basicConfig(level=logging.INFO)
    
    # --- Parse parameters ---
    # parameters = process_args(sys.argv[1:], Defaults)
    parameters = process_args([], Defaults)
    if parameters.deterministic:
        rng = np.random.RandomState(123456)
    else:
        rng = np.random.RandomState()
    
    # --- Instantiate environment ---
    env = Toy_env(rng, settings)

    # --- Instantiate qnetwork ---
    qnetwork = MyQNetwork(
        env,
        parameters.rms_decay,
        parameters.rms_epsilon,
        parameters.momentum,
        parameters.clip_norm,
        parameters.freeze_interval,
        parameters.batch_size,
        parameters.update_rule,
        rng)
    
    train_policy = EpsilonGreedyPolicy(qnetwork, env.nActions(), rng, 0.1)
    test_policy = EpsilonGreedyPolicy(qnetwork, env.nActions(), rng, 0.)

    # --- Instantiate agent ---
    agent = NeuralAgent(
        env,
        qnetwork,
        parameters.replay_memory_size,
        max(env.inputDimensions()[i][0] for i in range(len(env.inputDimensions()))),
        parameters.batch_size,
        rng, 
        train_policy=train_policy,
        test_policy=test_policy)

    # --- Bind controllers to the agent ---
    # Before every training epoch (periodicity=1), we want to print a summary of the agent's epsilon, discount and 
    # learning rate as well as the training epoch number.
    agent.attach(bc.VerboseController(
        evaluate_on='epoch', 
        periodicity=1))

    # During training epochs, we want to train the agent after every [parameters.update_frequency] action it takes.
    # Plus, we also want to display after each training episode (!= than after every training) the average bellman
    # residual and the average of the V values obtained during the last episode, hence the two last arguments.
    agent.attach(bc.TrainerController(
        evaluate_on='action', 
        periodicity=parameters.update_frequency, 
        show_episode_avg_V_value=True, 
        show_avg_Bellman_residual=True))

    # Every epoch end, one has the possibility to modify the learning rate using a LearningRateController. Here we 
    # wish to update the learning rate after every training epoch (periodicity=1), according to the parameters given.
    agent.attach(bc.LearningRateController(
        initial_learning_rate=parameters.learning_rate,
        learning_rate_decay=parameters.learning_rate_decay,
        periodicity=1))

    # Same for the discount factor.
    agent.attach(bc.DiscountFactorController(
        initial_discount_factor=parameters.discount,
        discount_factor_growth=parameters.discount_inc,
        discount_factor_max=parameters.discount_max,
        periodicity=1))

    # As for the discount factor and the learning rate, one can update periodically the parameter of the epsilon-greedy
    # policy implemented by the agent. This controllers has a bit more capabilities, as it allows one to choose more
    # precisely when to update epsilon: after every X action, episode or epoch. This parameter can also be reset every
    # episode or epoch (or never, hence the resetEvery='none').
    agent.attach(bc.EpsilonController(
        initial_e=parameters.epsilon_start, 
        e_decays=parameters.epsilon_decay, 
        e_min=parameters.epsilon_min,
        evaluate_on='action', 
        periodicity=1, 
        reset_every='none'))

    # We also want to interleave a "test epoch" between each training epoch. 
    # For each test epoch, we want also to display the sum of all rewards obtained, hence the showScore=True.
    # Finally, we want to call the summarizePerformance method of Toy_Env every [parameters.period_btw_summary_perfs]
    # *test* epochs.
    agent.attach(bc.InterleavedTestEpochController(
        id=0, 
        epoch_length=parameters.steps_per_test, 
        periodicity=1, 
        show_score=True,
        summarize_every=parameters.period_btw_summary_perfs))
        
    # --- Run the experiment ---
    agent.run(parameters.epochs, parameters.steps_per_epoch)



argv = sys.argv
while len(argv) > 0 and (argv[0].startswith("python") or argv[0].endswith(".py")):
    argv = argv[1:]

logging.info("arguments: " + json.dumps(argv))
logging.info("arguments: " + json.dumps(len(argv)))
if len(argv) < 4:
    print("All arguments are required!")
    print("arguments: <history_size> <caches_size> <data_path> <mask_nr>")
    print("  history_size: positive number")
    print("  caches_size: The number of items in the cache")
    print("  data_path: path to the queryset")
    print("  mask_nr: number which binary representation denotes which features are on and off")
    sys.exit(0)


# print(sys.argv)
# history_size = 1
history_size = int(argv[0])
caches_size = int(argv[1])
data_path = argv[2]
mask_nr = int(argv[3])

# history_size = 6
# caches_size = 10000
# data_path = "/storage/wdps/trident/experiments/results/query_sets/25000_10.json"
# mask_nr = 1010

total_measurements = 0
for sample in load_data(data_path):
    total_measurements += len(sample["q"]["measurements"])

# Defaults.EPOCHS = 50
Defaults.EPOCHS = 20
Defaults.STEPS_PER_TEST = int((total_measurements / 2) / Defaults.EPOCHS) - 1
Defaults.STEPS_PER_EPOCH = int((total_measurements / 2) / Defaults.EPOCHS) - 1


# print({"history_size": history_size,
# "caches_size": caches_size,
# "data_path": data_path,
# "mask_nr": mask_nr})

# print(json.dumps({
#     "field_count": len(Observation.blank().to_list()),
#     "field_names": list(Observation.blank().__dict__.keys())
# }))
setup = {
    "options":{
        "history_size": history_size,
        "caches_size": caches_size,
        "data_path": data_path,
        "mask_nr": mask_nr
    },
    "total_field_count": len(Observation.blank().to_list()),
    "total_field_names": list(Observation.blank().__dict__.keys()),
    "enabled_field_names": [],
    "disabled_field_names": [],
    "STEPS_PER_TEST": Defaults.STEPS_PER_TEST,
    "STEPS_PER_EPOCH": Defaults.STEPS_PER_EPOCH,
    "EPOCHS": Defaults.EPOCHS,
}

# # settings = Settings(data_path, caches_size, Observation.blank(), history_size)
settings = Settings.generate_settings(data_path, caches_size, mask_nr,
                history_size)

for field in settings.observation_mask.__dict__:
    if settings.observation_mask.__getattribute__(field) == 1:
        setup["enabled_field_names"].append(field)
    else:
        setup["disabled_field_names"].append(field)

print("### SETUP ###", json.dumps(setup))


start_experiment(settings)