import json
base_raw = """
{
    "name": "base-query-500",
    "description": "Running queries on database generated without skiptables parameter, no algorithms applied",
    "github_url": "https://github.com/pjotrscholtze/trident.git",
    "github_checkout": "master",
    "script": [
        "#!/bin/bash -e",
        "#SBATCH -t 15:00 -N 1 -n 8 --mem=16000M",
        "#SLURM -p longq",
        "#SBATCH --output=$PROJECT_PATH/slurm_%j.out",
        "du -h -d0 $DATABASE_PATH/latest-lexemes",
        "$BUILD_CACHE_PATH/trident/trident benchmark -i $DATABASE_PATH/latest-lexemes --query_type query_native --query_file $BUILD_CACHE_PATH/trident/experiments/queries/queries-500/query_chunk_0.sparql --results_file $PROJECT_PATH/res.json.lines --repetitions 30",
        "rm -rf $PROJECT_PATH/trident"
    ]
}
"""

res = []
for i in range(0, 913):
    data = json.loads(base_raw)
    data["name"] = "base-query-%d-500" % i
    data["script"][4] = "$BUILD_CACHE_PATH/trident/trident benchmark -i $DATABASE_PATH/latest-lexemes --query_type query_native --query_file $BUILD_CACHE_PATH/trident/experiments/queries/queries-500/query_chunk_%d.sparql --results_file $PROJECT_PATH/res.json.lines --repetitions 30" % i
    res.append(data)

with open("projects/base-query-500.json", "w") as f:
    f.writelines([json.dumps(res, indent=2)])