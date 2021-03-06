import json
base_raw = """
{
    "name": "simulation-hist-2-%d",
    "description": "Using different histogram approaches for index selection. Index out of bounds error in equiwidth and not enought time for voptimal.",
    "github_url": "https://github.com/pjotrscholtze/trident.git",
    "github_checkout": "master",
    "script": [
        "#!/bin/bash -e",
        "#SBATCH -t 720:00 -N 1 -n 8 --mem=64000M",
        "#SBATCH -p longq",
        "#SBATCH --output=$PROJECT_PATH/slurm_%j.out",
        "du -h -d0 $DATABASE_PATH/dbpedia-times-details-nindices-1",
        "# __REPLACED_BELOW__",
        "# __REPLACED_BELOW__",
        "__REPLACED_BELOW__"
    ]
}
"""


reruns = [47, 28, 55, 20, 11, 9, 10, 46, 38, 18, 19, 31, 36, 32, 37, 56, 54, 29, 45, 5, 27]
res = []
i = 0
# for i in range(0, int(9128 * 0.15)): # sample
for seed in [10, 4156, 2536, 2123, 7058, 1087, 8306]:
    for cmd in [
        "python main.py 25000 0.1 SEED 2 equi_width",
        "python main.py 25000 0.2 SEED 2 equi_width",
        "python main.py 25000 0.3 SEED 2 equi_width",

        "python main.py 25000 0.1 SEED 2 v_optimal",
        "python main.py 25000 0.2 SEED 2 v_optimal",
        "python main.py 25000 0.3 SEED 2 v_optimal",

        "python main.py 25000 0.1 SEED 2 maxdiff",
        "python main.py 25000 0.2 SEED 2 maxdiff",
        "python main.py 25000 0.3 SEED 2 maxdiff",
        ]:
        cmd = cmd.replace("SEED", str(seed))
        data = json.loads(base_raw)
        data["name"] = data["name"] % i
        # python/3.6.0
        data["script"][5] = "module load python/3.6.0"
        data["script"][6] = "source $BUILD_CACHE_PATH/venv/bin/activate"
        data["script"][7] = "python3 $BUILD_CACHE_PATH/trident/experiments/simulation/histogram/main.py %s" % cmd
        if i in reruns: res.append(data)
        i+=1


    with open("projects/simulation-hist-2.json", "w") as f:
        f.writelines([json.dumps(res, indent=2)])