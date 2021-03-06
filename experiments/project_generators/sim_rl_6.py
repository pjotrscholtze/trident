import json
base_raw = """
{
    "name": "sim-rl-6-%d",
    "description": "RL setup with deer, first batch. Fixed missing results display.",
    "github_url": "https://github.com/pjotrscholtze/trident.git",
    "github_checkout": "master",
    "script": [
        "#!/bin/bash -e",
        "#SBATCH -t 720:00 -N 1 -n 8 --mem=64000M",
        "#SBATCH -p longq",
        "#SBATCH --output=$PROJECT_PATH/slurm_%j.out",
        "module load cuda10.0/toolkit && module load cuDNN/cuda10.0 && source /home/pse740/.bashrc && activate && du -h -d0 $DATABASE_PATH/dbpedia-times-details-nindices-1",
        "# __REPLACED_BELOW__",
        "# __REPLACED_BELOW__",
        "__REPLACED_BELOW__"
    ]
}
"""


res = []
i = 0
BASE_MASK = (2**24) - 1
# for i in range(0, int(9128 * 0.15)): # sample
for seed in [10]:#, 4156, 2536, 2123, 7058, 1087, 8306]:
    # 2**Settings.count_observation_features()
    for cache_size in [2*1000*1000, 2000*1000*1000, 2000*1000*1000*1000]:
        for history_size in [1, 6]:
            mask = 0
            data = json.loads(base_raw)
            # /var/scratch/pse740/cache/query_sets/25000_
            cmd = "%d %d /var/scratch/pse740/cache/query_sets/25000_%s.json %d %s" % (history_size, cache_size, seed, BASE_MASK ^ mask, ("/var/scratch/pse740/rl_results/sim-rl-6_%d.json" % i))
            # cmd = "%d %d /storage/wdps/trident/experiments/results/query_sets/25000_%s.json %d" % (history_size, cache_size, seed, mask)
            data["name"] = data["name"] % i
            # python/3.6.0
            # data["script"][5] = "conda create --name rl_%d tensorflow==2.5.0 keras==2.4.3 numpy " % i
            data["script"][6] = "pip list"
            # data["script"][6] = "python3 -m pip install deer==0.4.3  && pip list"
            # data["script"][6] = "source $BUILD_CACHE_PATH/venv_rl/bin/activate"
            # python3 run_toy_env_multi.py 6 1000 /storage/wdps/trident/experiments/results/query_sets/25000_10.json 1001
            data["script"][7] = "python3 $BUILD_CACHE_PATH/trident/experiments/simulation/rl/run_toy_env_multi.py %s" % cmd
            i += 1
            res.append(data)

            mask = 1
            for _ in range(0, 24):
                data = json.loads(base_raw)
                # /var/scratch/pse740/cache/query_sets/25000_
                cmd = "%d %d /var/scratch/pse740/cache/query_sets/25000_%s.json %d %s" % (history_size, cache_size, seed, BASE_MASK ^ mask, ("/var/scratch/pse740/rl_results/sim-rl-6_%d.json" % i))
                # cmd = "%d %d /storage/wdps/trident/experiments/results/query_sets/25000_%s.json %d" % (history_size, cache_size, seed, mask)
                data["name"] = data["name"] % i
                # python/3.6.0
                # data["script"][5] = "conda create --name rl_%d tensorflow==2.5.0 keras==2.4.3 numpy " % i
                data["script"][6] = "pip list"
                # data["script"][6] = "python3 -m pip install deer==0.4.3  && pip list"
                # data["script"][6] = "source $BUILD_CACHE_PATH/venv_rl/bin/activate"
                # python3 run_toy_env_multi.py 6 1000 /storage/wdps/trident/experiments/results/query_sets/25000_10.json 1001
                data["script"][7] = "python3 $BUILD_CACHE_PATH/trident/experiments/simulation/rl/run_toy_env_multi.py %s" % cmd
                res.append(data)


                mask <<= 1
                i +=1
print(i)

#     # cmd = "python main.py 25000 RATIO SEED 2 ALGO full".replace("RATIO", str(ratio)).replace("SEED", seed).replace("ALGO", algo)
#     for cmd in [
#         "6 1000 /storage/wdps/trident/experiments/results/query_sets/25000_10.json 1001",
#         " 25000 0.2 SEED 2 equi_width full $PROJECT_PATH/sim_stats.json",
#         " 25000 0.3 SEED 2 equi_width full $PROJECT_PATH/sim_stats.json",

#         " 25000 0.1 SEED 2 v_optimal full $PROJECT_PATH/sim_stats.json",
#         " 25000 0.2 SEED 2 v_optimal full $PROJECT_PATH/sim_stats.json",
#         " 25000 0.3 SEED 2 v_optimal full $PROJECT_PATH/sim_stats.json",

#         " 25000 0.1 SEED 2 maxdiff full $PROJECT_PATH/sim_stats.json",
#         " 25000 0.2 SEED 2 maxdiff full $PROJECT_PATH/sim_stats.json",
#         " 25000 0.3 SEED 2 maxdiff full $PROJECT_PATH/sim_stats.json",
#         ]:
#         cmd = cmd.replace("SEED", str(seed))
#         data = json.loads(base_raw)
#         data["name"] = data["name"] % i
#         # python/3.6.0
#         data["script"][5] = "module load python/3.6.0"
#         data["script"][6] = "source $BUILD_CACHE_PATH/venv/bin/activate"
#         # python3 run_toy_env_multi.py 6 1000 /storage/wdps/trident/experiments/results/query_sets/25000_10.json 1001
#         data["script"][7] = "python3 $BUILD_CACHE_PATH/trident/experiments/simulation/rl/run_toy_env_multi.py %s" % cmd
#         res.append(data)
#         i+=1


with open("projects/sim-rl-6.json", "w") as f:
    f.writelines([json.dumps(res, indent=2)])

# todo = json.loads("""
# {
#   "0.2-v_optimal-2123": true,
#   "0.3-v_optimal-2123": true,
#   "0.3-v_optimal-10": true,
#   "0.3-equi_width-4156": true
# }
# """)

# res = []
# i = 0
# for options in todo.keys():
#     parts = options.split("-")
#     ratio = parts[0]
#     algo = parts[1]
#     seed = parts[2]

#     cmd = "python main.py 25000 RATIO SEED 2 ALGO full".replace("RATIO", str(ratio)).replace("SEED", seed).replace("ALGO", algo)
#     data = json.loads(base_raw)
#     data["name"] = data["name"] % i
#     # python/3.6.0
#     data["script"][5] = "module load python/3.6.0"
#     data["script"][6] = "source $BUILD_CACHE_PATH/venv/bin/activate"
#     data["script"][7] = "python3 $BUILD_CACHE_PATH/trident/experiments/simulation/histogram/main.py %s" % cmd
#     i += 1
#     res.append(data)

# a=1

# with open("projects/simulation-hist-4.json", "w") as f:
#     f.writelines([json.dumps(res, indent=2)])