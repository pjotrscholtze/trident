# a = """{"hash": 2387965207819638404,"relativeQueryNumber": 0,"queryopti": 1.575386,"queryexec": 74.872456,"totalexec": 76.486526,"nResultingRows": 0,"indexCounter": [1,0,0,0,0,2],"finished": 1,"statsRow": 0,"statsColumn": 0,"statsCluster": 0,"aggrIndices": 0,"notAggrIndices": 1,"cacheIndices": 0,"spo": 0,"ops": 0,"pos": 0,"sop": 0,"osp": 0,"pso": 1}"""
import json
# print(json.dumps(json.loads(a), indent=2))

with open("/storage/wdps/trident/res.json.lines", "r") as f:
    lines = f.readlines()
    hashes = set()
    for line in lines:
        res = json.loads(line)
        hashes.add(res["hash"])
    print(len(lines), len(hashes))