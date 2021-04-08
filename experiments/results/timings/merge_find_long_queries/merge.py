import shutil
import os
from glob import glob
import json
per_ittr = {}

for p in glob("results/timings/find_long_queries_*/find_long_queries_*/*"):
    key = int(p[34:35])
    if key not in per_ittr: per_ittr[key] = []
    per_ittr[key].append(p[55:].split("-")[1])

res = {}
for k in sorted(per_ittr.keys()):
    for i in per_ittr[k]:
        res[i] = k

for i in res:
    k = res[i]
    print("k", k, "i",i)
    if not os.path.exists("/storage/wdps/trident/experiments/results/timings/merge_find_long_queries/results/find_long_queries-%s" % i):
        os.mkdir("/storage/wdps/trident/experiments/results/timings/merge_find_long_queries/results/find_long_queries-%s" % i)
    for p in glob("results/timings/find_long_queries_%d/find_long_queries_%d/find_long_queries_%d-%s/*" %(k, k, k, i) ):
        file_name = (p[len("results/timings/find_long_queries_%d/find_long_queries_%d/find_long_queries_%d-%s/" %(k, k, k, i)):])
        new_path = ("/storage/wdps/trident/experiments/results/timings/merge_find_long_queries/results/find_long_queries-%s/%s" % (i, file_name))
        shutil.copy(p, new_path)
