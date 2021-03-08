import json
base_raw = """
{
    "name": "histogram-generate-per-query-%d-500-dbpedia-cleaned-queries-first-round",
    "description": "Generate histogram/counters for index and table usage, repetition will be 5 times (generate the stats per query), using dbpedia database, removed some queries that crashed or made the experiment take toolong",
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

updating_queries = ['/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_331.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_203.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_108.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_819.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_64.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_634.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_537.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_520.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_172.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_166.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_842.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_603.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_312.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_526.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_124.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_7.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_821.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_606.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_801.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_141.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_439.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_421.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_820.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_252.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_749.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_577.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_174.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_121.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_19.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_400.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_671.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_666.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_392.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_890.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_131.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_367.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_517.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_676.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_83.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_748.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_407.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_516.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_192.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_431.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_21.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_297.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_16.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_267.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_36.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_783.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_852.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_257.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_195.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_419.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_774.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_683.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_418.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_652.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_868.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_328.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_305.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_447.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_243.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_844.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_78.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_409.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_622.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_238.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_672.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_746.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_685.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_646.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_515.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_77.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_449.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_3.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_874.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_253.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_240.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_274.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_894.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_489.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_454.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_106.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_771.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_362.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_299.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_790.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_67.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_307.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_13.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_695.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_196.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_66.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_144.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_663.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_910.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_709.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_224.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_731.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_519.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_690.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_295.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_473.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_471.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_125.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_105.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_254.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_892.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_679.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_539.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_416.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_777.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_726.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_465.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_178.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_609.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_370.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_714.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_45.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_725.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_490.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_584.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_463.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_430.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_384.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_154.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_319.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_762.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_287.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_656.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_272.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_34.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_232.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_276.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_626.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_369.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_110.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_487.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_420.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_2.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_311.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_544.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_300.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_130.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_470.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_581.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_858.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_807.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_851.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_651.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_488.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_383.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_119.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_814.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_712.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_889.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_63.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_6.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_836.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_766.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_301.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_345.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_754.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_674.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_265.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_264.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_82.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_304.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_68.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_686.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_65.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_256.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_406.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_402.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_882.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_589.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_28.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_511.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_352.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_388.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_809.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_59.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_135.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_863.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_263.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_151.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_602.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_289.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_76.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_429.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_824.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_472.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_729.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_357.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_58.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_351.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_793.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_617.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_508.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_697.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_480.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_859.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_653.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_164.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_359.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_33.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_707.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_883.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_514.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_308.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_733.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_564.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_25.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_356.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_554.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_887.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_100.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_38.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_27.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_818.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_769.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_205.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_512.sparql', '/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_199.sparql']

# print([int(p[len("/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_"):-len(".sparql")])for p in updating_queries])
res = []
for i in [int(p[len("/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_"):-len(".sparql")])for p in updating_queries]:
    data = json.loads(base_raw)
    data["name"] = data["name"] % i
    data["script"][5] = "$BUILD_CACHE_PATH/trident/trident benchmark -i $DATABASE_PATH/dbpedia --query_type query_native --query_file $BUILD_CACHE_PATH/trident/experiments/queries_cleaned_first_round/queries-500/query_chunk_%d.sparql --results_file $PROJECT_PATH/res.json.lines --histogram_mode generate --histogram_file $PROJECT_PATH/temp.json --repetitions 5" % i
    res.append(data)

# print(len(updating_queries))

with open("projects/histogram-generate-per-query-500-dbpedia-cleaned-queries-first-round.json", "w") as f:
    f.writelines([json.dumps(res, indent=2)])