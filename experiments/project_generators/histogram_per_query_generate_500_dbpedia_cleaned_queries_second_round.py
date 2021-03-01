import json
base_raw = """
{
    "name": "histogram-generate-per-query-%d-500-dbpedia-cleaned-queries-second-round",
    "description": "Generate histogram/counters for index and table usage, repetition will be 5 times (generate the stats per query), using dbpedia database, removed some queries that crashed or made the experiment take toolong, round two of finding these",
    "github_url": "https://github.com/pjotrscholtze/trident.git",
    "github_checkout": "master",
    "script": [
        "#!/bin/bash -e",
        "#SBATCH -t 15:00 -N 1 -n 8 --mem=16000M",
        "#SBATCH -p longq",
        "#SBATCH --output=$PROJECT_PATH/slurm_%j.out",
        "du -h -d0 $DATABASE_PATH/dbpedia",
        "__REPLACED_BELOW__"
    ]
}
"""

updating_queries = ['/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_400.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_652.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_517.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_783.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_514.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_7.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_836.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_263.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_295.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_238.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_3.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_690.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_6.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_402.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_178.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_144.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_842.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_419.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_584.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_420.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_844.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_746.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_265.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_581.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_67.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_516.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_383.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_663.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_19.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_254.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_108.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_276.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_801.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_859.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_488.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned_second_round/query_chunk_695.sparql']

# print([int(p[len("/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_"):-len(".sparql")])for p in updating_queries])
res = []
for i in [int(p[len("/storage/wdps/trident/experiments/queries_second_round/queries_cleaned/query_chunk_"):-len(".sparql")])for p in updating_queries]:
    data = json.loads(base_raw)
    data["name"] = data["name"] % i
    data["script"][5] = "$BUILD_CACHE_PATH/trident/trident benchmark -i $DATABASE_PATH/dbpedia --query_type query_native --query_file $BUILD_CACHE_PATH/trident/experiments/queries_cleaned_second_round/queries-500/query_chunk_%d.sparql --results_file $PROJECT_PATH/res.json.lines --histogram_mode generate --histogram_file $PROJECT_PATH/temp.json --repetitions 5" % i
    res.append(data)

# print(len(updating_queries))

with open("projects/histogram-generate-per-query-500-dbpedia-cleaned-queries-second-round.json", "w") as f:
    f.writelines([json.dumps(res, indent=2)])