import json, logging, os, py7zr, random, sys
from typing import Dict, List
from glob import glob
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
    files = glob("/var/scratch/pse740/acquire_measurements_full-fast-*/res.json.lines.7z")
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

def load_queries(with_buckets):
    logging.info("Start loading query data")
    for i, path in enumerate(with_buckets):
        logging.info("Loading query data chunk @%d/%d (%.2f perc) with %d queries" % (i, len(with_buckets), (i/len(with_buckets)) * 100, len(with_buckets[path])))
        for index, q in get_data(path, with_buckets[path]):
            yield path_to_int(path), index, q
    logging.info("Finished loading query data")


def path_to_int(path): return int(path[89:].split("/")[0])

def get_data(filepath: str, index: List) -> List[Dict[str, any]]:
    # filepath = "/storage/wdps/trident/experiments" + filepath[1:]
    filepath = "/var/scratch/pse740/" + (filepath[61:].replace("acquire_measurements_sample", "acquire_measurements_full-fast"))

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


#
# MAIN
#
argv = sys.argv
while argv[0].startswith("python") or argv[0].endswith(".py"):
    argv = argv[1:]

logging.info("arguments: " + json.dumps(argv))
logging.info("arguments: " + json.dumps(len(argv)))

if len(argv) < 4:
    print("All arguments are required!")
    print("arguments: <amount> <training_ratio> <seed> <output_path>")
    print("  amount: positive number")
    print("  training_ratio: between 0.0 and 1.0")
    print("  seed: any integer")
    print("  output_path: Path to the output file.")
    sys.exit(0)


AMOUNT = int(argv[0])
TRAINING_RATIO = float(argv[1])
SEED = int(argv[2])
OUTPUT_PATH = argv[3]


# AMOUNT = 25000
# AMOUNT = 25
# TRAINING_RATIO = 0.1
# SEED = 1

with_buckets, ordered_query_locations = get_buckets_locations(AMOUNT, TRAINING_RATIO, SEED)
raw_queries = None

logging.info("hah")
res = [{"q":q,"path":path,"qid":qid} for path, qid, q in load_queries(with_buckets)]
with open(OUTPUT_PATH, "w") as f:
    json.dump(res, f, separators=(',', ':'))
# print(json.dumps(res))
# sys.exit(0)
