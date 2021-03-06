import json
base_raw = """
{
    "name": "base-query-skiptables",
    "description": "Running queries on database generated with skiptables parameter, no algorithms applied",
    "github_url": "https://github.com/pjotrscholtze/trident.git",
    "github_checkout": "master",
    "script": [
        "#!/bin/bash -e",
        "#SBATCH -t 120:00 -N 1 -n 8 --mem=16000M",
        "#SBATCH --output=$PROJECT_PATH/slurm_%j.out",
        "du -h -d0 $DATABASE_PATH/latest-lexemes-skipTables",
        "$BUILD_CACHE_PATH/trident/trident benchmark -i $DATABASE_PATH/latest-lexemes-skipTables- --query_type query_native --query_file $BUILD_CACHE_PATH/trident/experiments/queries/queries/query_chunk_0.sparql --results_file $PROJECT_PATH/res.json.lines --repetitions 30",
        "rm -rf $PROJECT_PATH/trident"
    ]
}
"""

res = []
for i in range(0,92):
    data = json.loads(base_raw)
    data["name"] = "base-query-%d-skiptables" % i
    data["script"][4] = "$BUILD_CACHE_PATH/trident/trident benchmark -i $DATABASE_PATH/latest-lexemes-skipTables --query_type query_native --query_file $BUILD_CACHE_PATH/trident/experiments/queries/queries/query_chunk_%d.sparql --results_file $PROJECT_PATH/res.json.lines --repetitions 30" % i
    res.append(data)

with open("projects/base-query-skiptables.json", "w") as f:
    f.writelines([json.dumps(res, indent=2)])