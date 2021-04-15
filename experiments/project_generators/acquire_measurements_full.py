import json
base_raw = """
{
    "name": "acquire_measurements_full-%d",
    "description": "Single repitition, database generated with a single index. These jobs run longer then normal, watch this with the scheduler. Full to get all measurements of query time table generation.",
    "github_url": "https://github.com/pjotrscholtze/trident.git",
    "github_checkout": "master",
    "script": [
        "#!/bin/bash -e",
        "#SBATCH -t 30:00 -N 1 -n 8 --mem=64000M",
        "#SBATCH -p longq",
        "#SBATCH --output=$PROJECT_PATH/slurm_%j.out",
        "du -h -d0 $DATABASE_PATH/dbpedia-times-details-nindices-1",
        "__REPLACED_BELOW__",
        "7z a $PROJECT_PATH/res.json.lines.7z $PROJECT_PATH/res.json.lines",
        "rm $PROJECT_PATH/res.json.lines"
    ]
}
"""



res = []
# for i in range(0, int(9128 * 0.15)): # sample
for i in range(0, 9128): # full
    data = json.loads(base_raw)
    data["name"] = data["name"] % i
    data["script"][5] = "$BUILD_CACHE_PATH/trident/trident benchmark -i $DATABASE_PATH/dbpedia-times-details-nindices-1 --query_file $BUILD_CACHE_PATH/trident/experiments/queries_full_small_chunks_max_2min_v6/query_chunk_%d.sparql --results_file $PROJECT_PATH/res.json.lines --histogram_mode generate --histogram_file $PROJECT_PATH/temp.json --repetitions 1" % i
    res.append(data)

with open("projects/acquire_measurements_full.json", "w") as f:
    f.writelines([json.dumps(res, indent=2)])