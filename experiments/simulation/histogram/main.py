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

# /**
#  * @author herald
#  */
class Histogram:

    def __init__(self, partition_rule: PartitionRule):
        self.partition_rule = partition_rule
        self.algorithm: ConstructionAlgorithm = ConstructionAlgorithmFactory.get_algorithm(partition_rule)

    def create_histogram(self, data: List[tuple[any,float]],
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
    CACHE_PATH = "/tmp/trident_get_buckets.tmp"
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r")as f:
            return json.load(f)

    def _(resline_path, size=65536):
        archive = py7zr.SevenZipFile(resline_path, mode='r')
        fp = archive.read(archive.list()[0].filename)[archive.list()[0].filename]
        while True:
            block = fp.read(size)
            if not block: break
            yield block
        # res[resline_path] = len(archive.read(archive.list()[0].filename)[archive.list()[0].filename].readlines())
        archive.close()

    res = {}
    # MATCHER = bytes("\n", 'utf-8')
    files = glob("/storage/wdps/trident/experiments/results/acquiremeasurements/acquire_measurements_sample.7z/acquire_measurements_sample-*/res.json.lines.7z")
    for i, resline_path in enumerate(sorted(files)):
        logging.info("Processing: (%.1f procent) %s" % ((i/len(files)) * 100, resline_path))
        # for s in _(resline_path):
        #     print(s.count(b'\n'))
        res[resline_path] =  sum([s.count(b'\n') for s in _(resline_path)])
        logging.info("Found %d queries" % res[resline_path])
        # archive = py7zr.SevenZipFile(resline_path, mode='r')
        # res[resline_path] = len(archive.read(archive.list()[0].filename)[archive.list()[0].filename].readlines())
        # archive.close()
    with open(CACHE_PATH, "w")as f:
        json.dump(res, f)
    return res

class QueryPicker:
    def __init__(self, seed):
        self._buckets = get_buckets()
        self._rnd = random.Random()
        # self._rnd.randint
        self._rnd.seed(seed)

    def get_single(self):
        keys = list(self._buckets.keys())
        key = keys[self._rnd.randint(0, len(keys) - 1)]
        return (key, self._rnd.randint(0, self._buckets[key]))

    def get_bunch(self, amount):
        for i in range(0, amount):
            yield self.get_single()
    
    # def get(self, amount):
    #     res = {}
    #     for path, index in self.get_bunch(amount):
    #         if path not in res: res[path] = []
    #         res[path].append(index)
    #     return res

def get_data(filepath: str, index: List) -> List[Dict[str, any]]:
    filepath = "/storage/wdps/trident/experiments" + filepath[1:]
    archive = py7zr.SevenZipFile(filepath, mode='r')

    fp = archive.read(archive.list()[0].filename)[archive.list()[0].filename]
    line = fp.readline()
    i = 0
    res = None
    while line and index:
        if i in index:
            index.pop(index.index(i))
            if len(line) > 1024 * 1024 * 100: continue
            # line = b"," + line[line.index(b"measurements\":[")+15:-3]
            # measurements = []
            # while line.endswith(b"}"):
            #     # print(line)
            #     if b"},{" in line:
            #         current = line[:line.index(b"},{")+1][1:].decode("utf-8")
            #         line = line[line.index(b"},{")+1:]
            #     else:
            #         current = line[1:].decode("utf-8")
            #         line = b"a"
            #         pass
            #     measurements.append(json.loads(current))
                
                # a=1
            yield i, json.loads(line)#["measurements"]
        i += 1
        line = fp.readline()
        
    # print(archive.list()[0].filename)
    # # archive.extractall(path="/tmp")
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
    # raw_queries = {}

    logging.info("Start loading query data")
    for i, path in enumerate(with_buckets):
        logging.info("Loading query data chunk @%d/%d (%.2f perc) with %d queries" % (i, len(with_buckets), (i/len(with_buckets)) * 100, len(with_buckets[path])))
        # raw_queries[path_to_int(path)] = {}
        for index, q in get_data(path, with_buckets[path]):
            yield path_to_int(path), index, q
            # raw_queries[path_to_int(path)][index] = q
    logging.info("Finished loading query data")
    # return raw_queries

def get_histogram(data, bucket_count):
    hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.equi_width))
    # hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.v_optimal))
    # hist = Histogram(PartitionRule(PartitionClass.serial, PartitionConstraint.maxdiff))
    return  hist.create_histogram(data, bucket_count)

def get_histogram_breakpoint(histogram):
    bucket_count = len(histogram)
    import math
    index_breakpoint = math.ceil(bucket_count * 0.2)
    min_values = [e[1] for e in histogram[index_breakpoint].data]
    max_values = [e[1] for e in histogram[index_breakpoint-1].data]
    # print("min_values", min_values)
    # print("max_values", max_values)
    # print("avg1", sum(min_values + max_values) / (len(min_values)+ len(max_values)))
    # print("avg2", (max(min_values) + min(max_values)) / 2)
    # print("avg3", (max(min_values)*1.99 + min(max_values)*0.01) / 2)
    # print(max(min_values))
    # # for bucket in histogram
    # pass
    return (max(min_values) + min(max_values)) / 2

def measurement_hash(measurement):
    return "idx%ds%dp%do%dtermList%d" % (measurement["idx"], measurement["s"], measurement["p"], measurement["o"], measurement["termList"])


if __name__ == "__main__":
    AMOUNT = 1500
    TRAINING_RATIO = 0.2
    SEED = 10
    BUCKET_COUNT = 2
    with_buckets, ordered_query_locations = get_buckets_locations(AMOUNT, TRAINING_RATIO, SEED)
    raw_queries = None

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
        },
        "cache_hashes": []
    }


    training_count = int(AMOUNT * TRAINING_RATIO)
    logging.info("Start training on %d queries" % (training_count))
    training_paths = {}
    traing_buckets = {}
    for i in range(0, training_count):
        path, index = ordered_query_locations[i]
        if path_to_int(path) not in training_paths:
            training_paths[path_to_int(path)] = []
        if path not in traing_buckets: traing_buckets[path] = []
        traing_buckets[path].append(index)
        training_paths[path_to_int(path)].append(index)
    training_measurements = []
    tmp = {k: [e for e in traing_buckets[k]] for k in traing_buckets}
    for chunk_id, index, q in load_queries(tmp):
        # if chunk_id in training_paths and index in training_paths[chunk_id]:
        # metrics = raw_queries[path][str(index)]
        for measurement in q["measurements"]:
            if measurement["duration"] == 0: continue
            training_measurements.append([1, measurement["duration"], measurement])

    # import sys
    # sys.exit(0)
    # with open("/tmp/temp_with_buckets15000.json", "w") as f:
    #     json.dump(load_queries(with_buckets), f)
    # with open("/tmp/temp_with_buckets15000.json", "r") as f:
    #     raw_queries = json.load(f)

    # training_count = int(AMOUNT * TRAINING_RATIO)
    # logging.info("Start training on %d queries" % (training_count))
    # training_measurements = []
    # for i in range(0, training_count):
    #     path, index = ordered_query_locations[i]
    #     if str(index) not in raw_queries[path]: continue
    #     metrics = raw_queries[path][str(index)]
    #     for measurement in metrics["measurements"]:
    #         training_measurements.append([1, int(measurement["duration"])])
    logging.info("Building histogram")

    # hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.equi_width))
    # hist = Histogram(PartitionRule(PartitionClass.end_biased, PartitionConstraint.v_optimal))
    # hist = Histogram(PartitionRule(PartitionClass.serial, PartitionConstraint.maxdiff))
    # test = hist.create_histogram(training_measurements, BUCKET_COUNT)
    test  = get_histogram(training_measurements, BUCKET_COUNT)
    # print(json.dumps([e.data for e in test], indent=2))
    breakpoint = get_histogram_breakpoint(test)
    # print("breakpoint", breakpoint)
    logging.info("using breakpoint value of %.3f" %breakpoint)

    cache = []

    for m in training_measurements:
        measurement = m[2]
        if int(measurement["duration"]) >= breakpoint:
            hash = measurement_hash(measurement)
            if hash not in cache: cache.append(hash)
    stats["cache_hashes"] = [] + cache

    # tmp = {}
    # tmp = {k: [e for e in traing_buckets[k]] for k in traing_buckets}
    # for chunk_id, index, q in load_queries(tmp):
    #     print(q)
    #     pass

    # for i in range(0, training_count):
    #     path, index = ordered_query_locations[i]
    #     if str(index) not in raw_queries[path]: continue
    #     metrics = raw_queries[path][str(index)]
    #     for measurement in metrics["measurements"]:
    #         if int(measurement["duration"]) >= breakpoint:
    #             hash = measurement_hash(measurement)
    #             # hash = "idx%ds%dp%do%dtermList%d" % (measurement["idx"], measurement["s"], measurement["p"], measurement["o"], measurement["termList"])
    #             if hash not in cache: cache.append(hash)
    logging.info("Selected %d items for caching" % len(cache))


    eval_buckets = {}
    for i in range(training_count, AMOUNT - 1):
        path, index = ordered_query_locations[i]
        if path not in eval_buckets: eval_buckets[path] = []
        eval_buckets[path].append(index)

    logging.info("Evaluating")
    tmp = {k: [e for e in eval_buckets[k]] for k in eval_buckets}
    for chunk_id, index, q in load_queries(tmp):
        stats["eval_time_all"] += q["totalexec"]
        stats["eval_query_count"] += 1
        stats["eval_queries_with_table_generation"] += int(len(q["measurements"]) != 0)
        stats["eval_table_generations_all"] += len(q["measurements"])
        stats["eval_table_generations_all_time"] += sum([m["duration"] for m in q["measurements"]])
        
        # if chunk_id in training_paths and index in training_paths[chunk_id]:
        # metrics = raw_queries[path][str(index)]
        for measurement in q["measurements"]:
            if measurement["duration"] < breakpoint: continue
            if measurement_hash(measurement) not in cache: continue
            stats["eval_table_generations_skipped"] += 1
            stats["eval_table_generations_skipped_time"] += measurement["duration"]

    print(json.dumps(stats, indent=2))


    # cache_hits_hashes = []
    # cache_hits_queries = []
    # for i in range(training_count, AMOUNT-1):
    #     path, index = ordered_query_locations[i]
    #     if str(index) not in raw_queries[path]: continue
    #     metrics = raw_queries[path][str(index)]
    #     # print(metrics["measurements"])
    #     for measurement in metrics["measurements"]:
    #         if measurement_hash(measurement) in cache:
    #             print(measurement)
    #         training_measurements.append([1, int(measurement["duration"] * 1000 * 1000)])

    # training_count = int(AMOUNT * TRAINING_RATIO)
    # logging.info("Start training on %d queries" % (training_count))
    # for i in range(0, training_count):
    #     path, index = ordered_query_locations[i]
    #     print(raw_queries[path][index])
    a=1
    # training_data = []
    # testing_data = []
    # training_data_threshold = TRAINING_RATIO * AMOUNT
    # training_phase = True
    # i = 0
    # for path, index in qp.get_bunch(AMOUNT):
    #     print(path,index)
        # logging.info("%d perc" % ((i / AMOUNT) * 100))
        # data_single = get_data(path, index)
        # if training_phase:
        #     training_phase = i <= training_data_threshold
        #     if not training_phase:
        #         logging.info("Finished gathering training data!")
        #         logging.info("Loading testing data")
        #     training_data.append(data_single)
        # else: testing_data.append(data_single)
        # i += 1

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


