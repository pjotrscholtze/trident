import json
base_raw = """
{
    "name": "find_long_queries_6-%d",
    "description": "find_long_queries first itteration of this, using a single repitition, database generated with a single index. These jobs run longer then normal, watch this with the scheduler. Round 6.",
    "github_url": "https://github.com/pjotrscholtze/trident.git",
    "github_checkout": "master",
    "script": [
        "#!/bin/bash -e",
        "#SBATCH -t 30:00 -N 1 -n 8 --mem=64000M",
        "#SBATCH -p longq",
        "#SBATCH --output=$PROJECT_PATH/slurm_%j.out",
        "du -h -d0 $DATABASE_PATH/dbpedia-times-details-nindices-1",
        "__REPLACED_BELOW__"
    ]
}
"""



res = []
for i in [8077,7030,6314,7402,4450,2865,2976,2878,1876,4372,8140,5956,948,894,4329,4495,3471,3728,824,3549]:
    data = json.loads(base_raw)
    data["name"] = data["name"] % i
    data["script"][5] = "$BUILD_CACHE_PATH/trident/trident benchmark -i $DATABASE_PATH/dbpedia-times-details-nindices-1 --query_file $BUILD_CACHE_PATH/trident/experiments/queries_full_small_chunks_max_2min_v6/query_chunk_%d.sparql --results_file $PROJECT_PATH/res.json.lines --histogram_mode generate --histogram_file $PROJECT_PATH/temp.json --repetitions 1" % i
    res.append(data)

with open("projects/find_long_queries_6.json", "w") as f:
    f.writelines([json.dumps(res, indent=2)])