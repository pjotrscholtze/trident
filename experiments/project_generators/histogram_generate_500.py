import json
base_raw = """
{
    "name": "histogram-generate-%d-500",
    "description": "Generate histogram/counters for index and table usage, repetition will be 5 times",
    "github_url": "https://github.com/pjotrscholtze/trident.git",
    "github_checkout": "master",
    "script": [
        "#!/bin/bash -e",
        "#SBATCH -t 15:00 -N 1 -n 8 --mem=16000M",
        "#SLURM -p longq",
        "#SBATCH --output=$PROJECT_PATH/slurm_%j.out",
        "du -h -d0 $DATABASE_PATH/latest-lexemes-skipTables",
        "__REPLACED_BELOW__"
    ]
}
"""

res = []
for i in range(0, 913):
    data = json.loads(base_raw)
    data["name"] = data["name"] % i
    data["script"][5] = "$BUILD_CACHE_PATH/trident/trident benchmark -i $DATABASE_PATH/latest-lexemes-skipTables --query_type query_native --query_file $BUILD_CACHE_PATH/trident/experiments/queries/queries-500/query_chunk_%d.sparql --results_file $PROJECT_PATH/res.json.lines --repetitions 5" % i
    res.append(data)

with open("projects/histogram-generate-500.json", "w") as f:
    f.writelines([json.dumps(res, indent=2)])