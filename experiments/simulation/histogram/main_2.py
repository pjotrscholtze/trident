# /**
#  * Copyright MaDgIK Group 2010 - 2015.
#  */
from typing import List, Dict
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s[%(levelname)s]%(message)s")
from bucketNumberGenerator import BucketNumberGenerator
from bucketNumberGenerator.LinearBucketNumberGenerator import LinearBucketNumberGenerator
from constructionAlgorithm.ConstructionAlgorithm import ConstructionAlgorithm
from constructionAlgorithm.ConstructionAlgorithmFactory import ConstructionAlgorithmFactory
from partitionRule.PartitionRule import PartitionRule
from partitionRule.PartitionClass import PartitionClass
from partitionRule.PartitionConstraint import PartitionConstraint
from score.HistogramScore import HistogramScore
from score.MinimizeVarianceHistogramScore import MinimizeVarianceHistogramScore
from score.BalanceVarianceAndBucketsHistogramScore import BalanceVarianceAndBucketsHistogramScore

from Bucket import Bucket
from glob import glob
import json
import random
import py7zr
import os
import sys

def load_table_sizes(path):
    # path = "/storage/wdps/trident/experiments/get_tablesizes/results.json"
    # /storage/wdps/trident/experiments/get_tablesizes/results.json
    with open(path) as f:
        return json.load(f)
def load_data(path):
    # "/storage/wdps/trident/experiments/results/query_sets/25000_10.json"
    with open(path) as f:
        return json.load(f)


# /**
#  * @author herald
#  */
class Histogram:

    def __init__(self, partition_rule: PartitionRule):
        self.partition_rule = partition_rule
        self.algorithm: ConstructionAlgorithm = ConstructionAlgorithmFactory.get_algorithm(partition_rule)

    # def create_histogram(self, data: List[tuple[any,float]],
    #     bucketNum: int = None, score: HistogramScore = None,
    #     generator: BucketNumberGenerator= None) -> List[Bucket]:
    def create_histogram(self, data: List,
        bucketNum: int = None, score: HistogramScore = None,
        generator: BucketNumberGenerator= None) -> List[Bucket]:
        """
        :param: data:      The dataset with <key,value> pairs.
        :param: bucketNum: The number of buckets (option 1).
        :param: score:     (option 2).
        :param: generator: (option 2).
        :return: A list of buckets (option 1). The histogram with the maximum
                 score (option 2).
        """
        if bucketNum is not None:
            return self.algorithm.create_histogram(data, bucketNum, self.partition_rule)

        best: List[Bucket] = None
        bestScore: float = 0
        while generator.has_next():
            next: int = generator.get_next()
            if best is None:
                best = self.algorithm.create_histogram(data, next, self.partition_rule)
                bestScore = score.get_score(best)
                continue

            h: List[Bucket] = self.algorithm.create_histogram(data, next, self.partition_rule)
            s: float = score.get_score(h)

            logging.debug(str(bestScore) + "(" + str(len(best)) + ")" + " >=? " + str(s) + "(" + str(next) + ")")

            if s > bestScore:
                best = h
                bestScore = s

        return best


logging.basicConfig(level=logging.INFO)

def get_buckets() -> Dict[str, int]:
    CACHE_PATH = "/home/pse740/trident/trident_get_buckets.tmp"
    # CACHE_PATH = "/tmp/trident_get_buckets.tmp"
    if os.path.exists(CACHE_PATH):
        print("bucket cache not found: ", CACHE_PATH)
        with open(CACHE_PATH, "r")as f:
            return json.load(f)

    def _(resline_path, size=65536):
        archive = py7zr.SevenZipFile(resline_path, mode='r')
        fp = archive.read(archive.list()[0].filename)[archive.list()[0].filename]
        while True:
            block = fp.read(size)
            if not block: break
            yield block
        archive.close()

    res = {}
    # files = glob("/storage/wdps/trident/experiments/results/acquiremeasurements/acquire_measurements_sample.7z/acquire_measurements_sample-*/res.json.lines.7z")
    files = glob("/var/scratch/pse740/acquire_measurements_full-*/res.json.lines.7z")
    for i, resline_path in enumerate(sorted(files)):
        logging.info("Processing: (%.1f procent) %s" % ((i/len(files)) * 100, resline_path))
        res[resline_path] =  sum([s.count(b'\n') for s in _(resline_path)])
        logging.info("Found %d queries" % res[resline_path])
    with open(CACHE_PATH, "w")as f:
        json.dump(res, f)
    return res

class QueryPicker:
    def __init__(self, seed):
        self._buckets = get_buckets()
        self._rnd = random.Random()
        self._rnd.seed(seed)

    def get_single(self):
        keys = list(self._buckets.keys())
        key = keys[self._rnd.randint(0, len(keys) - 1)]
        return (key, self._rnd.randint(0, self._buckets[key]))

    def get_bunch(self, amount):
        for i in range(0, amount):
            yield self.get_single()
    
def get_data(filepath: str, index: List) -> List[Dict[str, any]]:
    # filepath = "/storage/wdps/trident/experiments" + filepath[1:]
    filepath = "/var/scratch/pse740/" + (filepath[61:].replace("acquire_measurements_sample", "acquire_measurements_full"))

    archive = py7zr.SevenZipFile(filepath, mode='r')

    fp = archive.read(archive.list()[0].filename)[archive.list()[0].filename]
    line = fp.readline()
    i = 0
    res = None
    while line and index:
        if i in index:
            index.pop(index.index(i))
            if len(line) > 1024 * 1024 * 100: continue
            yield i, json.loads(line)
        i += 1
        line = fp.readline()
        
    archive.close()



def get_buckets_locations(amount, training_ratio, seed):
    qp = QueryPicker(seed)
    logging.info("Selecting queries (%d), training size %d(%d perc), testing size %d(%d perc)" % (amount, training_ratio * amount, training_ratio * 100, (1 - training_ratio)* amount, (1 - training_ratio)*100))
    ordered = []
    with_buckets = {}
    for path, index in qp.get_bunch(amount):
        ordered.append((path, index))
        if path not in with_buckets: with_buckets[path] = []
        with_buckets[path].append(index)
    return with_buckets, ordered

def path_to_int(path): return int(path[89:].split("/")[0])

def load_queries(with_buckets):
    logging.info("Start loading query data")
    for i, path in enumerate(with_buckets):
        logging.info("Loading query data chunk @%d/%d (%.2f perc) with %d queries" % (i, len(with_buckets), (i/len(with_buckets)) * 100, len(with_buckets[path])))
        for index, q in get_data(path, with_buckets[path]):
            yield path_to_int(path), index, q
    logging.info("Finished loading query data")

def get_histogram(data, bucket_count, histogram_type):
    # hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.equi_width))
    # hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.v_optimal))
    # hist = Histogram(PartitionRule(PartitionClass.serial, PartitionConstraint.maxdiff))
    # test = hist.create_histogram(training_measurements, BUCKET_COUNT)

    hist = Histogram(PartitionRule(PartitionClass.end_biased, histogram_type))#PartitionConstraint.equi_width))
    # hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.v_optimal))
    # hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.maxdiff))
    if bucket_count > 0: 
        return hist.create_histogram(data, bucket_count)
    elif bucket_count == -1:
        return hist.create_histogram(data,
            score=MinimizeVarianceHistogramScore(),
            generator=LinearBucketNumberGenerator(1, 1, 3))
    elif bucket_count == -2:
        return hist.create_histogram(data,
            score=BalanceVarianceAndBucketsHistogramScore(1),
            generator=LinearBucketNumberGenerator(1, 1, 3))
    raise Exception("Invalid option given!")

def get_histogram_breakpoint(histogram):
    bucket_count = len(histogram)
    import math
    index_breakpoint = math.ceil(bucket_count * 0.2)
    min_values = [e[1] for e in histogram[index_breakpoint].data]
    max_values = [e[1] for e in histogram[index_breakpoint-1].data]
    return (max(min_values) + min(max_values)) / 2

def measurement_hash(measurement):
    return "idx%ds%dp%do%dtermList%d" % (measurement["idx"], measurement["s"], measurement["p"], measurement["o"], measurement["termList"])


if __name__ == "__main__":
    argv = sys.argv
    while argv[0].startswith("python") or argv[0].endswith(".py"):
        argv = argv[1:]

    logging.info("arguments: " + json.dumps(argv))
    logging.info("arguments: " + json.dumps(len(argv)))
    if len(argv) < 7:
        print("All arguments are required!")
        print("arguments: <amount> <training_ratio> <seed> <bucket_count> <histogram_type> <output_path>")
        print("  amount: positive number")
        print("  training_ratio: between 0.0 and 1.0")
        print("  seed: any integer")
        print("  bucket_count: -1, -2 for dynamic options or 0> for fixed number")
        print("  histogram_type: equi_width, v_optimal, or maxdiff")
        print("  simulation_type: full, or query_selection. Default: full")
        print("  output_path: Path to the output file.")
        sys.exit(0)

    AMOUNT = int(argv[0])
    TRAINING_RATIO = float(argv[1])
    SEED = int(argv[2])
    BUCKET_COUNT = int(argv[3])
    HISTOGRAM_TYPE = {
        "equi_width": PartitionConstraint.equi_width,
        "v_optimal": PartitionConstraint.v_optimal,
        "maxdiff": PartitionConstraint.maxdiff,
    }[argv[4]]
    SIMULATION_TYPE = argv[5]
    if SIMULATION_TYPE not in ["full", "query_selection"]: raise ValueError("Unkown simulation type")
    OUTPUT_PATH = argv[6]

    stats = {
        "eval_query_count": 0,
        "eval_queries_with_table_generation": 0,
        "eval_time_all": 0,
        "eval_table_generations_all": 0,
        "eval_table_generations_all_time": 0,
        "eval_table_generations_skipped": 0,
        "eval_table_generations_skipped_time": 0,
        "config": {
            "inspecting_queries_count": AMOUNT,
            "training_ratio": TRAINING_RATIO,
            "seed": SEED,
            "histogram_bucket_count": BUCKET_COUNT,
            "histogram_type": HISTOGRAM_TYPE.value,
            "simulation_type": SIMULATION_TYPE,
        },
        "cache_hashes": [],
        "eval_table_generations_skipped_queries": []
    }
    logging.info("arguments: " + json.dumps(sys.argv))
    logging.info("Running with config:")
    logging.info(json.dumps(stats["config"], indent=2))
    stats["config"]["histogram_type"] = HISTOGRAM_TYPE

    with_buckets, ordered_query_locations = get_buckets_locations(AMOUNT, TRAINING_RATIO, SEED)
    raw_queries = None

    if SIMULATION_TYPE == "query_selection":
        logging.info("hah")
        res = [q for _,_, q in load_queries(with_buckets)]
        print(json.dumps(ordered_query_locations))
        sys.exit(0)

    logging.info("Loading query set")
    # 
    query_set = load_data("/var/scratch/pse740/cache/query_sets/25000_%d.json" % SEED)

    training_count = int(AMOUNT * TRAINING_RATIO)
    logging.info("Start training on %d queries" % (training_count))
    # training_paths = {}
    # traing_buckets = {}
    # for i in range(0, training_count):
    #     path, index = ordered_query_locations[i]
    #     if path_to_int(path) not in training_paths:
    #         training_paths[path_to_int(path)] = []
    #     if path not in traing_buckets: traing_buckets[path] = []
    #     traing_buckets[path].append(index)
    #     training_paths[path_to_int(path)].append(index)
    training_measurements = []

    for i in range(0, training_count):
        training_measurements.append(query_set[i])
    # tmp = {k: [e for e in traing_buckets[k]] for k in traing_buckets}
    # for chunk_id, index, q in load_queries(tmp):
    #     for measurement in q["measurements"]:
    #         if measurement["duration"] == 0: continue
    #         training_measurements.append([1, measurement["duration"], measurement])

    logging.info("Building histogram")

    test  = get_histogram(training_measurements, BUCKET_COUNT, HISTOGRAM_TYPE)
    breakpoint = get_histogram_breakpoint(test)
    logging.info("using breakpoint value of %.3f" %breakpoint)


    table_sizes = load_table_sizes("/var/scratch/pse740/cache/table_size.json")

    def get_table_size(s, p, o):
        return table_sizes[str(s)][str(p)][str(o)]

    cache = []
    cache_size_base = 0

    for m in training_measurements:
        measurement = m[2]
        if int(measurement["duration"]) >= breakpoint:
            hash = measurement_hash(measurement)
            if hash not in cache:
                cache.append(hash)
                cache_size_base += get_table_size(measurement["s"], measurement["p"], measurement["o"])
    stats["cache_hashes"] = [] + cache

    logging.info("Selected %d items for caching" % len(cache))

    # eval_buckets = {}
    # for i in range(training_count, AMOUNT - 1):
    #     path, index = ordered_query_locations[i]
    #     if path not in eval_buckets: eval_buckets[path] = []
    #     eval_buckets[path].append(index)



    logging.info("Evaluating")
    # tmp = {k: [e for e in eval_buckets[k]] for k in eval_buckets}
    stats["eval_encountered_cache"] = {}
    stats["eval_sim_queries"] = {}
    stats["round2_slowest_table_generations_time"] = 0
    stats["round2_static_histogram_table_generations_time"] = [0]
    stats["round2_static_histogram_tables"] = cache
    stats["round2_dynamic_histogram_table_generations_time"] = [0]
    stats["round2_dynamic_histogram_tables"] = [] + cache
    stats["round2_dynamic_histogram_tables_size"] = [cache_size_base]

    stats["round2_dynamic_slim_start_histogram_table_generations_time"] = [0]
    stats["round2_dynamic_slim_start_histogram_tables"] = []
    stats["round2_dynamic_slim_start_histogram_tables_size"] = [0]


    for i in range(training_count, AMOUNT):
        q = query_set[i]

        # for chunk_id, index, q in load_queries(tmp):
        stats["eval_time_all"] += q["totalexec"]
        stats["eval_query_count"] += 1
        stats["eval_queries_with_table_generation"] += int(len(q["measurements"]) != 0)
        stats["eval_table_generations_all"] += len(q["measurements"])
        stats["eval_table_generations_all_time"] += sum([m["duration"] for m in q["measurements"]])

        stats["eval_sim_queries"][q["hash"]] = {
            "worst_ms": [],
            "simul_ms": [],
            "opti_totalexec": q["totalexec"],
            "opti_queryexec": q["queryexec"],
            "opti_queryopti": q["queryopti"],
            "cid": -1, #chunk_id,
            "ln": -1, #index, # Line Number
        }


        # Does not learn after learning phase!
        for measurement in q["measurements"]:
            current_measurement_hash = measurement_hash(measurement)
            table_size = get_table_size(measurement["s"], measurement["p"], measurement["o"])


            stats["round2_slowest_table_generations_time"] += measurement["duration"]
            if current_measurement_hash not in stats["round2_static_histogram_tables"]:
                stats["round2_static_histogram_table_generations_time"].append(stats["round2_static_histogram_table_generations_time"][-1] + measurement["duration"])

            if current_measurement_hash not in stats["round2_dynamic_histogram_tables"] and measurement["duration"] < breakpoint:
                stats["round2_dynamic_histogram_tables"].append(current_measurement_hash)
                stats["round2_dynamic_histogram_table_generations_time"].append(stats["round2_dynamic_histogram_table_generations_time"][-1] + measurement["duration"])
                stats["round2_dynamic_histogram_tables_size"].append(stats["round2_dynamic_histogram_tables_size"][-1] + table_size)

            if current_measurement_hash not in stats["round2_dynamic_slim_start_histogram_tables"] and measurement["duration"] < breakpoint:
                stats["round2_dynamic_slim_start_histogram_tables"].append(current_measurement_hash)
                stats["round2_dynamic_slim_start_histogram_table_generations_time"].append(stats["round2_dynamic_slim_start_histogram_table_generations_time"][-1] + measurement["duration"])
                stats["round2_dynamic_slim_start_histogram_tables_size"].append(stats["round2_dynamic_slim_start_histogram_tables_size"][-1] + table_size)




            stats["eval_sim_queries"][q["hash"]]["worst_ms"].append(measurement["duration"])
            # current_measurement_hash = measurement_hash(measurement)
            if measurement["duration"] < breakpoint: continue
            if current_measurement_hash not in cache: continue
            if current_measurement_hash not in stats["eval_encountered_cache"]:
                stats["eval_encountered_cache"][current_measurement_hash] = []
            stats["eval_encountered_cache"][current_measurement_hash].append(measurement["duration"])
            stats["eval_table_generations_skipped"] += 1
            stats["eval_table_generations_skipped_time"] += measurement["duration"]
            stats["eval_sim_queries"][q["hash"]]["simul_ms"].append(measurement["duration"])

        if q["measurements"]:
            stats["eval_table_generations_skipped_queries"].append(q)
            # stats["eval_table_generations_skipped_queries"].append({"chunk_id": chunk_id, "index": index})

    stats["config"]["histogram_type"] = stats["config"]["histogram_type"].value
    with open(OUTPUT_PATH, "w") as f:
        json.dump(stats, f, separators=(',',':') )
    # print(json.dumps(stats, separators=(',',':')))



    # import json
    # hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.maxdiff))
    # test = hist.create_histogram([
    #     [1, 2],
    #     [1, 2],
    #     [10, 2],
    #     [100, 1],
    # ], 2)
    # print(json.dumps([e.data for e in test], indent=2))
    # test = hist.create_histogram([
    #     [1, 2],
    #     [1, 2],
    #     [10, 2],
    #     [100, 1],
    # ], score= MinimizeVarianceHistogramScore(),
    #     generator= LinearBucketNumberGenerator(0, 1, 10))
    # print(json.dumps([e.data for e in test], indent=2))
    # test = hist.create_histogram([
    #     [1, 2],
    #     [1, 2],
    #     [10, 2],
    #     [100, 1],
    # ], score= BalanceVarianceAndBucketsHistogramScore(1),
    #     generator= LinearBucketNumberGenerator(0, 1, 10))
    # print(json.dumps([e.data for e in test], indent=2))

    # print("----")
    # print("----")
    # print("----")

    # hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.equi_width))
    # test = hist.create_histogram([
    #     [1, 2],
    #     [1, 2],
    #     [10, 2],
    #     [100, 1],
    # ], 2)
    # print(json.dumps([e.data for e in test], indent=2))
    # test = hist.create_histogram([
    #     [1, 2],
    #     [1, 2],
    #     [10, 2],
    #     [100, 1],
    # ], score= MinimizeVarianceHistogramScore(),
    #     generator= LinearBucketNumberGenerator(1, 1, 10))
    # print(json.dumps([e.data for e in test], indent=2))
    # test = hist.create_histogram([
    #     [1, 2],
    #     [1, 2],
    #     [10, 2],
    #     [100, 1],
    # ], score= BalanceVarianceAndBucketsHistogramScore(1),
    #     generator= LinearBucketNumberGenerator(1, 1, 10))

    # print("----")
    # print("----")
    # print("----")

    # hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.v_optimal))
    # test = hist.create_histogram([
    #     [1, 2],
    #     [1, 2],
    #     [10, 2],
    #     [100, 1],
    # ], 2)
    # print(json.dumps([e.data for e in test], indent=2))
    # # test = hist.create_histogram([
    # #     [1,2],
    # #     [1,2],
    # #     [10,2],
    # #     [100,1],
    # # ], score= MinimizeVarianceHistogramScore(),
    # #     generator= LinearBucketNumberGenerator(1, 1, 10))
    # # print(json.dumps([e.data for e in test], indent=2))
    # # test = hist.create_histogram([
    # #     [1,2],
    # #     [1,2],
    # #     [10,2],
    # #     [100,1],
    # # ], score= BalanceVarianceAndBucketsHistogramScore(1),
    # #     generator= LinearBucketNumberGenerator(1, 1, 10))
    # # print(json.dumps([e.data for e in test], indent=2))


