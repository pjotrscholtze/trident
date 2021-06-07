from glob import glob
import json
hashes = []
hashes_cid_ln = {}
for p_sim_stats in glob("/storage/wdps/trident/experiments/results/asim-hist-1/sim-hist-1-*/sim_stats.json"):
    print(p_sim_stats)
    with open(p_sim_stats, "r") as f:
        data  = json.load(f)
        for sq in data['eval_sim_queries']:
            if data['eval_sim_queries'][sq]['cid'] not in hashes_cid_ln:
                hashes_cid_ln[data['eval_sim_queries'][sq]['cid']] = []
            hashes_cid_ln[data['eval_sim_queries'][sq]['cid']].append(data['eval_sim_queries'][sq]['ln'])
            
        hashes += data['eval_sim_queries'].keys()

missing_hash = 0
missing_path = 0
total = 0
for p_qs in glob("/storage/wdps/trident/experiments/results/query_sets/25000_10.json"):
    with open(p_qs) as f:
        data = json.load(f)
        for q in data:
            total += 1

            missing_path += int(q['path'] in hashes_cid_ln and q['qid'] in hashes_cid_ln[q['path']])
            missing_hash += int(str(q['q']['hash']) not in hashes)
            # if str(q['q']['hash']) not in hashes:
            #     print(q['path'] in hashes_cid_ln and q['qid'] in hashes_cid_ln[q['path']])
            #     print(data[1]['q']['hash'])
        a=1
print("missing_path", missing_path)
print("missing_hash", missing_hash)
print("total", total)
a=1

pass

