import json
base_raw = """
{
    "name": "generate-dbpedia-db-times-skiptables",
    "description": "Generate dbpedia, get times for tables, with skiptables",
    "github_url": "https://github.com/pjotrscholtze/trident.git",
    "github_checkout": "master",
    "script": [
        "#!/bin/bash -e",
        "#SBATCH -t 150:00 -N 1 -n 8 --mem=64000M",
        "#SBATCH -p longq",
        "#SBATCH --output=$PROJECT_PATH/slurm_%j.out",
        "time $BUILD_CACHE_PATH/trident/trident load -i $DATABASE_PATH/dbpedia-times-skiptables -f /var/scratch/pse740/db/dbpedia_raw/file.nt.gz -l debug --skipTables true --thresholdSkipTable 0  2>&1",
        "du -h -d0 $DATABASE_PATH/dbpedia-times-skiptables"
    ]
}
"""
#"time $BUILD_CACHE_PATH/trident/trident load -i $DATABASE_PATH/latest-lexemes -f /var/scratch/pse740/latest-lexemes.nt.gz",


res = []
# for i in range(0, 913):
data = json.loads(base_raw)
# data["name"] = data["name"] % i
# data["script"][5] = "$BUILD_CACHE_PATH/trident/trident benchmark -i $DATABASE_PATH/latest-lexemes-skipTables --query_type query_native --query_file $BUILD_CACHE_PATH/trident/experiments/queries/queries-500/query_chunk_%d.sparql --results_file $PROJECT_PATH/res.json.lines --histogram_mode generate --histogram_file $PROJECT_PATH/temp.json --repetitions 5" % i
res.append(data)

with open("projects/generate-dbpedia-db-times-skiptables.json", "w") as f:
    f.writelines([json.dumps(res, indent=2)])