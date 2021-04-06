import json
base_raw = """
{
    "name": "find_long_queries_2-%d",
    "description": "find_long_queries first itteration of this, using a single repitition, database generated with a single index. These jobs run longer then normal, watch this with the scheduler. Round 2.",
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
for i in [7775,539,8077,7030,168,4367,3967,6544,6271,6505,8376,2076,7206,6314,5487,9051,3807,7402,5040,4431,5967,4450,6926,5348,427,2865,2976,3063,5850,2878,4636,6069,4784,4638,7406,1876,4372,1619,8140,3368,5956,7926,1324,1334,786,948,1299,7966,678,894,4329,5347,785,4495,3471,3728,824,3549]:
    data = json.loads(base_raw)
    data["name"] = data["name"] % i
    data["script"][5] = "$BUILD_CACHE_PATH/trident/trident benchmark -i $DATABASE_PATH/dbpedia-times-details-nindices-1 --query_file $BUILD_CACHE_PATH/trident/experiments/queries_full_small_chunks_max_2min_v2/query_chunk_%d.sparql --results_file $PROJECT_PATH/res.json.lines --histogram_mode generate --histogram_file $PROJECT_PATH/temp.json --repetitions 1" % i
    res.append(data)

with open("projects/find_long_queries_2.json", "w") as f:
    f.writelines([json.dumps(res, indent=2)])