import json
import os
from glob import glob
from typing import List
import shutil

def get_progress_lines(lines: List[str]):
    for line in lines:
        if line.endswith("/499\n"):
            yield line

faulty_queries = {
    "slow_queries": [],
    "slow_queries_string": [],
    "crashing_queries": [],
    "crashing_queries_string": [],
}
i = 0
reruns = []
for p in glob("results/histogram-generate-per-query-500-dbpedia-cleaned-queries-second-round/*"):
    if p == "results/histogram-generate-per-query-500-dbpedia-cleaned-queries-second-round/graphs": continue
    dst = "/storage/wdps/trident/experiments/queries/queries_cleaned_third_round/query_chunk_%s.sparql" % p.split("histogram-generate-per-query-")[2].split("-500-")[0]
    shutil.copy("/storage/wdps/trident/experiments/queries/queries_cleaned/query_chunk_%s.sparql" % p.split("histogram-generate-per-query-")[2].split("-500-")[0], 
        dst)
    if not os.path.exists(p + "/temp.json"):
        slurm = glob(p +"/slurm_*.out")[0]
        last_query = -1
        slow_query = False
        with open(slurm, "r") as f:
            lines = f.readlines()
            progress = list(get_progress_lines(lines))
            last_query = int(progress[len(progress)-1].strip().split("INFO")[1].strip().split("/")[0])
            # print(last_query)
            if lines[-1].endswith(" DUE TO TIME LIMIT ***\n"):
                # Slow queries
                faulty_queries["slow_queries"].append(last_query)
                slow_query = True
            else:
                # Crashing queries
                slow_query = False
                faulty_queries["crashing_queries"].append(last_query)
        lines = []
        with open(dst, "r") as f: lines = f.readlines()
        i = 0
        res_lines = []
        for line in lines:
            if i == last_query:
                if slow_query:
                    faulty_queries["slow_queries_string"].append(line)
                else:
                    faulty_queries["crashing_queries_string"].append(line)
            else: res_lines.append(line)
            i += 1
        # with open(dst, "w") as f:
        #     f.writelines(["".join(res_lines)])
        reruns.append(dst)

print(reruns)
# print(i)