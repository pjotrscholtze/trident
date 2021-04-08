import shutil
import os
from glob import glob
import json


# for p in glob("/storage/wdps/trident/experiments/results/timings/merge_find_long_queries/results/find_long_queries-*/res.json.lines"):
#     print(p)

total = 0
for p_base in glob("/storage/wdps/trident/experiments/results/timings/merge_find_long_queries/results/find_long_queries-*"):
    slurm = glob("%s/slurm*" % p_base)
    reslines = glob("%s/res.json.lines" % p_base)
    # if not slurm or not reslines:
    #     print(reslines, slurm)

    if not reslines: continue
    out = []
    with open(reslines[0], "r") as f: 
        for line in f.readlines():
            if not line: continue
            data = json.loads(line.strip())
            if not data["hash"]: continue
            # print(line)
            # print(json.loads(line.strip())["hash"])
            # total+=len(f.readlines())
            out.append(line)
            total+=1
    with open("%s/cleaned_lines.json.lines" % p_base, "w") as f:
        f.writelines("".join(out))
    # break

    # for p in glob("%s/res.json.lines" % p_base):
    #     print(p)
    # with open(p, "r") as f:
    #     lines = f.readlines()
    #     print("".join(lines[:-10]))
    #     print(p)
    # break
print(total)