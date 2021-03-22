import json
base_raw = """
{
    "name": "histogram-generate-per-query-%d-500-dbpedia-cleaned-full-all-indices",
    "description": "Generate histogram/counters for index and table usage, repetition will be 5 times (generate the stats per query), using dbpedia database, cleaned of crashing queries, run all queries",
    "github_url": "https://github.com/pjotrscholtze/trident.git",
    "github_checkout": "master",
    "script": [
        "#!/bin/bash -e",
        "#SBATCH -t 15:00 -N 1 -n 8 --mem=16000M",
        "#SBATCH -p longq",
        "#SBATCH --output=$PROJECT_PATH/slurm_%j.out",
        "du -h -d0 $DATABASE_PATH/dbpedia-times-details",
        "__REPLACED_BELOW__"
    ]
}
"""

res = []
for i in range(0, 913):
    data = json.loads(base_raw)
    data["name"] = data["name"] % i
    data["script"][5] = "$BUILD_CACHE_PATH/trident/trident benchmark -i $DATABASE_PATH/dbpedia-times-details --query_type query_native --query_file $BUILD_CACHE_PATH/trident/experiments/queries_full/query_chunk_%d.sparql --results_file $PROJECT_PATH/res.json.lines --histogram_mode generate --histogram_file $PROJECT_PATH/temp.json --repetitions 1" % i
    res.append(data)

with open("projects/histogram-generate-per-query-500-dbpedia-cleaned-full-all-indices.json", "w") as f:
    f.writelines([json.dumps(res, indent=2)])