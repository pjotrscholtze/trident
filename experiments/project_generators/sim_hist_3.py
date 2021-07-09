import json
base_raw = """
{
    "name": "sim-hist-3-%d",
    "description": "Using different histogram approaches for index selection. Index out of bounds error in equiwidth and not enought time for voptimal. Out of time issues. Added more details for statistics. And optimal performance overall stats",
    "github_url": "https://github.com/pjotrscholtze/trident.git",
    "github_checkout": "master",
    "script": [
        "#!/bin/bash -e",
        "#SBATCH -t 1440:00 -N 1 -n 16 --mem=64000M",
        "#SBATCH -p longq",
        "#SBATCH --output=$PROJECT_PATH/slurm_%j.out",
        "du -h -d0 $DATABASE_PATH/dbpedia-times-details-nindices-1",
        "# __REPLACED_BELOW__",
        "# __REPLACED_BELOW__",
        "__REPLACED_BELOW__"
    ]
}
"""


res = []
i = 0
# for i in range(0, int(9128 * 0.15)): # sample
for seed in [10, 4156, 2536, 2123, 7058, 1087, 8306]:
    # cmd = "python main.py 25000 RATIO SEED 2 ALGO full".replace("RATIO", str(ratio)).replace("SEED", seed).replace("ALGO", algo)
    for cmd in [
        "python main_2.py 25000 0.1 SEED 2 equi_width full $PROJECT_PATH/sim_stats.json",
        "python main_2.py 25000 0.2 SEED 2 equi_width full $PROJECT_PATH/sim_stats.json",
        "python main_2.py 25000 0.3 SEED 2 equi_width full $PROJECT_PATH/sim_stats.json",

        "python main_2.py 25000 0.1 SEED 2 v_optimal full $PROJECT_PATH/sim_stats.json",
        "python main_2.py 25000 0.2 SEED 2 v_optimal full $PROJECT_PATH/sim_stats.json",
        "python main_2.py 25000 0.3 SEED 2 v_optimal full $PROJECT_PATH/sim_stats.json",

        "python main_2.py 25000 0.1 SEED 2 maxdiff full $PROJECT_PATH/sim_stats.json",
        "python main_2.py 25000 0.2 SEED 2 maxdiff full $PROJECT_PATH/sim_stats.json",
        "python main_2.py 25000 0.3 SEED 2 maxdiff full $PROJECT_PATH/sim_stats.json",
        ]:
        cmd = cmd.replace("SEED", str(seed))
        data = json.loads(base_raw)
        data["name"] = data["name"] % i
        # python/3.6.0
        data["script"][5] = "module load python/3.6.0"
        data["script"][6] = "source $BUILD_CACHE_PATH/venv/bin/activate"
        data["script"][7] = "python3 $BUILD_CACHE_PATH/trident/experiments/simulation/histogram/main_2.py %s" % cmd
        res.append(data)
        i+=1


with open("projects/sim-hist-3.json", "w") as f:
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