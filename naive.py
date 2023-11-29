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
R = read_rnd_file('./rnd.txt')
seq1 = read_rnd_file('./seq1.txt')
seq2 = read_rnd_file('./seq2.txt')
Wk = []
for obj_id in R.keys():
    R[obj_id] += seq1.get(obj_id, 0) + seq2.get(obj_id, 0)
for obj_id, score in R.items():
    Wk.append((score, obj_id))
count_seq_access = len(seq1) + len(seq2)
result = sorted(Wk, key=lambda x: x[0], reverse=True)[:k]
time_end = time.time()
time_used = time_end - time_start
print("Naive Algorithm:")
print(f"Time used = {time_used} seconds")
print(f"Number of sequential accesses = {count_seq_access}")
print("Top k objects:")
for score, obj_id in result:
    print(f"{obj_id}: {score:.2f}")

# Naive Algorithm:
# Time used = 0.32363080978393555 seconds
# Number of sequential accesses = 200000
# Top k objects:
# 50905: 14.84
# 85861: 14.76
# 75232: 14.74
# 20132: 14.74
# 22652: 14.74