import heapq
from collections import defaultdict
import time 
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

seen_objects = defaultdict(float)
Wk = []
object_only_add_one_score=[]
count_seq_access = 0
T = float('inf')

for obj_id in R.keys():
    for seq_id in [1,2]:
        if seq_id==1:
            seq=seq1
            obj_id, score = next(seq)
            obj_id1, score1 = obj_id, score
            count_seq_access += 1
        else:
            seq=seq2
            obj_id, score = next(seq)
            obj_id2, score2 = obj_id, score
            count_seq_access += 1

        if obj_id in seen_objects:
            seen_objects[obj_id] += score
            object_only_add_one_score.remove(obj_id)
            if len(Wk)<k:
                heapq.heappush(Wk, (seen_objects[obj_id],obj_id))
            else:
                heapq.heappushpop(Wk, (seen_objects[obj_id],obj_id))
        else:
            seen_objects[obj_id] = score + R[obj_id]
            object_only_add_one_score.append(obj_id)

    if len(Wk) == k:
        T=score1+score2+R[obj_id]

    if Wk and Wk[0][0]>= T:
            can_terminate = True
            for id, lower_bound in seen_objects.items():
                if id in object_only_add_one_score:
                    lower_bound=lower_bound+max(score1,score2)
                if id not in list(dict(Wk).values()) and lower_bound>Wk[0][0]:
                    can_terminate = False
                    break
            if can_terminate:
                break

result = sorted(Wk, key=lambda x: x[0], reverse=True)
time_end=time.time()
time_used=time_end-time_start

print("TA Algorithm:")
print(f"Time used = {time_used} seconds")
print(f"Number of sequential accesses = {count_seq_access}")
print("Top k objects:")
for score,obj_id in result:
    print(f"{obj_id}: {score:.2f}")

# TA Algorithm:
# Time used = 0.179671049118042 seconds
# Number of sequential accesses = 3018
# Top k objects:
# 50905: 14.84
# 85861: 14.76
# 22652: 14.74
# 75232: 14.74
# 20132: 14.74


