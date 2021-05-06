# python3 simulation/histogram/main.py python main.py 25000 0.1 10 2 equi_width query_selection >> /storage/wdps/trident/experiments/asim_querieshash_10.json
# python3 simulation/histogram/main.py python main.py 25000 0.1 4156 2 equi_width query_selection >> /storage/wdps/trident/experiments/asim_querieshash_4156.json
# python3 simulation/histogram/main.py python main.py 25000 0.1 2536 2 equi_width query_selection >> /storage/wdps/trident/experiments/asim_queries_hash_2536.json
# python3 simulation/histogram/main.py python main.py 25000 0.1 2123 2 equi_width query_selection >> /storage/wdps/trident/experiments/asim_queries_hash_2123.json
# python3 simulation/histogram/main.py python main.py 25000 0.1 7058 2 equi_width query_selection >> /storage/wdps/trident/experiments/asim_queries_hash_7058.json
# python3 simulation/histogram/main.py python main.py 25000 0.1 1087 2 equi_width query_selection >> /storage/wdps/trident/experiments/asim_queries_hash_1087.json
# python3 simulation/histogram/main.py python main.py 25000 0.1 8306 2 equi_width query_selection >> /storage/wdps/trident/experiments/asim_queries_hash_8306.json



import json
base_raw = """
{
    "name": "get_project_hashes-%d",
    "description": "Get the hashes for the queries used in the different simulations.",
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


reruns = [45, 10, 46, 38, 54, 47, 18, 11, 28, 56, 20, 32, 55, 31, 9, 29, 37, 5, 27, 36]
res = []
i = 0
# for i in range(0, int(9128 * 0.15)): # sample
for seed in [10, 4156, 2536, 2123, 7058, 1087, 8306]:
    # for cmd in [
    #     "python main.py 25000 0.1 SEED 2 equi_width",
    #     "python main.py 25000 0.2 SEED 2 equi_width",
    #     "python main.py 25000 0.3 SEED 2 equi_width",

    #     "python main.py 25000 0.1 SEED 2 v_optimal",
    #     "python main.py 25000 0.2 SEED 2 v_optimal",
    #     "python main.py 25000 0.3 SEED 2 v_optimal",

    #     "python main.py 25000 0.1 SEED 2 maxdiff",
    #     "python main.py 25000 0.2 SEED 2 maxdiff",
    #     "python main.py 25000 0.3 SEED 2 maxdiff",
    #     ]:
    cmd = "main.py 25000 0.1 SEED 2 equi_width query_selection"
    cmd = cmd.replace("SEED", str(seed))
    data = json.loads(base_raw)
    data["name"] = data["name"] % i
    # python/3.6.0
    data["script"][5] = "module load python/3.6.0"
    data["script"][6] = "source $BUILD_CACHE_PATH/venv/bin/activate"
    data["script"][7] = "python3 $BUILD_CACHE_PATH/trident/experiments/simulation/histogram/main.py %s" % cmd
    # if i in reruns:
    res.append(data)
    i+=1


    with open("projects/get_project_hashes.json", "w") as f:
        f.writelines([json.dumps(res, indent=2)])