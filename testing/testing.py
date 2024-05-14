import matplotlib.pyplot as plt
from simulate1 import simulate as default
from simulate2 import simulate as multithread
from simulate3 import simulate as numba
from simulate4 import simulate as max_perf

implementations = [(default, "default"), (multithread, "multithread"), (numba, "numba"), (max_perf, "max_perf")]

def general_test(m, n, ghosts, cherries, broken, seed, end, step, criteria):
    if criteria == 1: # size
        inputs = [[m + i*step, n + i*step, ghosts, cherries, broken, seed] for i in range((end-m)//step)]
    elif criteria == 2: # all scaler
        inputs = [[m + i*step, n + i*step, ghosts, cherries + i*step, broken + i*2*step, seed] for i in range((end-m)//step)]
    elif criteria == 3: # cherries
        inputs = [[m, n, ghosts, cherries + i*step, broken, seed] for i in range((end-cherries)//step)]
    elif criteria == 4:  # broken walls
        inputs = [[m, n, ghosts, cherries, broken + i*step, seed] for i in range((end-broken)//step)]
    elif criteria == 5:  # seed
        inputs = [[m, n, ghosts, cherries, broken, seed + i*step] for i in range((end-seed)//step)]
    else:
        print("Select criteria from 1 to 5")
        return None

    with open("res.txt", 'w', encoding='utf-8') as file:
        for item in inputs:
            print(item)
            line = test_criteria(*item)
            item = " ".join(map(lambda x:str(x),item))
            file.write(item)
            line = ([", ".join(map(lambda x: str(x), res)) for res in line])
            line = "\n".join(line)
            file.write(line)

            

def test_criteria(m, n, ghosts, cherries, broken, seed):
    results = []
    for impl, name in implementations:
        mini_res = impl(m, n, ghosts, cherries, broken, seed)
        mini_res[-1] = round(mini_res[-1], 2)
        mini_res[-1] = round(mini_res[-1], 2)
        print(mini_res)
        results.append(mini_res)
    return results

general_test(25, 25, 4, 25, 50, 10, 50, 5, 2)