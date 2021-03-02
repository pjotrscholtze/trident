import json
from glob import glob

res = {
    "spoStats.statsRow": 0,     "spoStats.statsColumn": 0,
    "spoStats.statsCluster": 0, "opsStats.statsRow": 0,
    "opsStats.statsColumn": 0,  "opsStats.statsCluster": 0,
    "posStats.statsRow": 0,     "posStats.statsColumn": 0,
    "posStats.statsCluster": 0, "sopStats.statsRow": 0,
    "sopStats.statsColumn": 0,  "sopStats.statsCluster": 0,
    "ospStats.statsRow": 0,     "ospStats.statsColumn": 0,
    "ospStats.statsCluster": 0, "psoStats.statsRow": 0,
    "psoStats.statsColumn": 6,  "psoStats.statsCluster": 0
}

i = 0
# 
for p in glob("results/histogram-generate-per-query-500-dbpedia-cleaned-queries-second-round/*/temp.json"):
    i += 1
    with open(p, "r") as f:
        for line in f.readlines():
            data = json.loads(line)
            for k in data:
                res[k] += data[k]


header = list(res.keys())
csv_rows = [
    header,
    [str(res[k]) for k in header]
]
with open("histogram-generate-per-query-500-dbpedia.combined.second-round.csv", "w") as f:
    f.writelines(["\n".join([",".join(line) for line in csv_rows])])