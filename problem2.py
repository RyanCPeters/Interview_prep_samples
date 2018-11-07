import os
import random
import itertools
import time
import concurrent.futures as cf
import tempfile

def solution(A):
    idx_starts = [0, 0]
    i = 1
    back = len(A)-1
    # start by identifying the first 2 types of fruit we can encounter
    while A[i]==A[idx_starts[0]] and i<len(A)-1:
        i += 1
    if i==len(A):
        # we got lucky and the entire list contained 2 or fewer fruit types
        return i-idx_starts[0]
    z = back-1
    while A[z] == A[back] and z > 0:
        z-=1
    back_pair = [A[z],A[back]]
    stop = z+1
    start = i
    idx_starts[1] = i
    cur_types = (A[idx_starts[0]], A[idx_starts[1]])
    a = i
    while a < len(A)-1 and A[a+1] in cur_types:
        a+=1
    while z > 0 and A[z-1] in back_pair:
        z-=1
    best_range = max(back-z+1, a+1)
    if best_range == len(A):
        return best_range
    # we now have the index locations for the first two types of fruit
    for j,v in enumerate(A[start:stop], start=start):
        if v not in cur_types:
            if j-idx_starts[0]>best_range:
                best_range = j-idx_starts[0]
            idx_starts[0] = idx_starts[1]
            idx_starts[1] = j
            cur_types = (A[idx_starts[0]], v)
    return best_range


def build_pair_sequence(r:int)->tuple:
    if not r or r < 1:
        return None, None
    src = random.sample(range(1000000000), r)
    seq_size = len(src)
    target_types = (src.pop(), src.pop())
    expected = seq_size//5
    target_seq = list(itertools.combinations_with_replacement(target_types, expected).__next__())
    base_seq = list(itertools.combinations(src, seq_size-expected).__next__())
    
    insert_at = random.randint(0,seq_size-expected)
    base_seq[insert_at:insert_at] = target_seq
    
    return (base_seq,expected)


if __name__ == "__main__":
    blk = "\x1b[90m|\x1b[m"
    color_wheel = {0:"{:>2}", 1:"\x1b[92m{:>2}\x1b[m", 2:"\x1b[31m{:>2}\x1b[m",
                   3:"\x1b[96m{:>2}\x1b[m", 4:"\x1b[94m{:>2}\x1b[m", 5:"\x1b[95m{:>2}\x1b[m"}
    # color_wheel = {0:"\x1b[92m{:>2}\x1b[m", 1:"\x1b[31m{:>2}\x1b[m",
    #                2:"\x1b[96m{:>2}\x1b[m", 3:"\x1b[94m{:>2}\x1b[m", 4:"\x1b[95m{:>2}\x1b[m"}
    

    samples = []
    # samples.append([[1,1,1,2,2,2,2,3,3,4,4,5,5],7])
    # samples.append([[1,2,1,2,1,2,1],7])
    samples.append([[1, 2, 5, 6, 4, 5,2,2,2, 3, 4, 6, 5, 6, 4, 6, 5, 1, 6, 6, 2, 1, 4, 6, 1, 6, 6, 4],4])
    samples.append([[1,2,1,3,4,3,5,1,2],3])
    samples.append([[1,1,1,2,2,2,2,2,2,1,1,1,1,2,5,1, 2, 5, 6, 4, 5,1, 2, 5, 6, 4, 5,1,1,1,1,1,1,1,1,1,1, 2, 5, 6, 4, 5],14])
    samples.append([[1, 2, 5, 6, 4, 5,1, 2, 5, 6, 4, 5,1,1,1,1,1,1,1,1,1, 2, 5, 6, 4, 5,1,1,1,2,2,2,2,2,2,1,1,1,1,2],14])
    samples.append([[1,1,1,2,2,2,2,2,2,1,1,1,1,2,5,1, 2, 5, 6, 4, 5,1, 2, 5, 6, 4, 5,1,1,1,1,1,1,1,1,1,1, 2, 5, 6, 4, 5,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11],21])
    for sample in samples:
        expected = sample[1]
        rng = range(len(sample[0]))
        print("[", "{:>2}".format(rng[0]), sep="", end="")
        for v in rng[1:]:
            print(blk,"{:>2}".format(v), sep="", end="")
        print("]")

        print("[", color_wheel[sample[0][0]%6].format(sample[0][0]), sep="", end="")
        for v in sample[0][1:]:
            print(blk,color_wheel[v%6].format(v), sep="", end="")
        print("]")
        time.sleep(.05)
        strt = time.time()
        res = solution(sample[0])
        end = time.time()-strt
        print("result   = {}\nexpected = {}".format(res, expected))
        print("time was: {}\n\n".format(end))
    del strt, end, res, sample, samples
    if True:
        time.sleep(.5)
        print("generating randomized sample sets now")
        solution_time_list = []
        alt_time_list = []
        solution_error_list = []
        alt_error_list = []
        with cf.ProcessPoolExecutor(6) as ppe:
            futs = []
            for r in range(1,1001):
                futs.append(ppe.submit(build_pair_sequence, r*100))
    
            while any([f.running() for f in futs]):
                time.sleep(.05)
            results = [f.result() for f in futs]
        time.sleep(1)
        print("testing on randomized sets now")
        count = 1
        for f in futs:
            sample = f.result()
            # sample = build_pair_sequence(random.sample(range(1000000000),r))
            expected = sample[1]
            # rng = range(len(sample))
            # print("[", "{:>2}".format(rng[0]), sep="", end="")
            # for v in rng[1:]:
            #     print(blk,"{:>2}".format(v), sep="", end="")
            # print("]")
            #
            # print("[", color_wheel[sample[0][0]%6].format(sample[0][0]), sep="", end="")
            # for v in sample[0][1:]:
            #     print(blk,color_wheel[v%6].format(v), sep="", end="")
            # print("]")
            strt = time.time()
            res = solution(sample[0])
            solution_time_list.append(time.time() - strt)
            
            count +=1
            
            # if res != expected:
            #     print("result   = {}\nexpected = {}\n\n".format(res, expected))
            #     print("time was: {}".format(end))
        print("\nbase solution performance")
        print("max time was: {}".format(max(solution_time_list)))
        print("average time was: {}".format(sum(solution_time_list)/len(solution_time_list)))
        print("number of errors was: {}".format(sum([x[1] for x in solution_error_list if not x[0]])))
        
