import json
base_raw = """
{
    "name": "get_sample_set_fast-%d",
    "description": "Get a sample queries set from the total queries set, saves some time later on.",
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



res = []
i = 0
# for i in range(0, int(9128 * 0.15)): # sample
for seed in [10, 4156, 2536, 2123, 7058, 1087, 8306]:
    for cmd in [
        "25000 0.1 SEED $BUILD_CACHE_PATH/query_sets/25000_SEED_fast.json",
        ]:
        cmd = cmd.replace("SEED", str(seed))
        data = json.loads(base_raw)
        data["name"] = data["name"] % i
        # python/3.6.0
        data["script"][5] = "module load python/3.6.0"
        data["script"][6] = "source $BUILD_CACHE_PATH/venv/bin/activate"
        data["script"][7] = "python3 $BUILD_CACHE_PATH/trident/experiments/simulation/get_sample_set_fast.py %s" % cmd
        res.append(data)
        i+=1


    with open("projects/get_sample_set_fast.json", "w") as f:
        f.writelines([json.dumps(res, indent=2)])