import heapq
from collections import defaultdict
import time 
import numpy as np
from tqdm import tqdm
def read_rnd_file(filename):
    R = {}
    with open(filename, 'r') as file:
        for line in file:
            obj_id, score = map(float, line.strip().split())
            R[int(obj_id)] = score
    return R

def seq_generator(filename):
    with open(filename, 'r') as file:
        for line in file:
            obj_id, score = map(float, line.strip().split())
            yield int(obj_id), score
time_start=time.time()
k=5
R = read_rnd_file('rnd.txt')
seq1 = seq_generator('seq1.txt')
seq2 = seq_generator('seq2.txt')

visited = defaultdict(lambda: -np.ones(3))
ub_lb = np.zeros((len(R),2))
seen_objects = defaultdict(float)
_score = [0, 0, 0]
_obj_id = [-1, -1, -1]
_seq = [R, seq1, seq2]
count_seq_access = 0
Wk = []
max_ub = 0
lb = []


for obj_id in tqdm(R.keys()):
    _obj_id[0] = obj_id
    _score[0] = R[obj_id]
    visited[obj_id][0] = R[obj_id]
    for seq_id in [1,2]:
        _obj_id[seq_id], _score[seq_id] = next(_seq[seq_id])
        count_seq_access += 1
        visited[_obj_id[seq_id]][seq_id] = _score[seq_id]
    for i in range(3):
        # import ipdb; ipdb.set_trace()
        ub_lb[_obj_id[i]][1] = ub_lb[_obj_id[i]][1] + _score[i]
        ub_lb[_obj_id[i]][0] = ub_lb[_obj_id[i]][1]
        if visited[_obj_id[i]].min()==-1:
            for j in range(3):
                if visited[_obj_id[i]][j]==-1:
                    ub_lb[_obj_id[i]][0] = ub_lb[_obj_id[i]][0] + _score[j]
        # import ipdb; ipdb.set_trace()
        if len(lb) < k:
            heapq.heappush(lb, (ub_lb[_obj_id[i]][1], _obj_id[i]))
        else:
            heapq.heappushpop(lb, (ub_lb[_obj_id[i]][1], _obj_id[i]))
        if _obj_id[i] not in lb and ub_lb[_obj_id[i]][1] > max_ub:
            max_ub = ub_lb[_obj_id[i]][1]

    if len(lb) >= k:
        #  ipdb; ipdb.set_trace()
        min_lb = lb[0][0]
        if min_lb >= max_ub:
            print("Terminating and reporting lb as top-k result:")
            break
# import ipdb; ipdb.set_trace()
result = sorted(lb, key=lambda x: visited[x[1]].sum(), reverse=True)
time_end=time.time()
time_used=time_end-time_start

print("NRA Algorithm:")
print(f"Time used = {time_used} seconds")
print(f"Number of sequential accesses = {count_seq_access}")
print("Top k objects:")
for score, obj_id in result:
    print(f"{obj_id}: {visited[obj_id].sum():.2f}")

# TA Algorithm:
# Time used = 0.179671049118042 seconds
# Number of sequential accesses = 3018
# Top k objects:
# 50905: 14.84
# 85861: 14.76
# 22652: 14.74
# 75232: 14.74
# 20132: 14.74
