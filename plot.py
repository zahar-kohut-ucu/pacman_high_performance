import matplotlib.pyplot as plt

filename = "./results/brwalls_criteria_numba.txt"
workers = 2
result = [[] for _ in range(workers)]
params = []
names1 = ['sequantial', 'multithreading', 'numba', 'max_perf']
names2 = ['numba', 'max_perf']
with open(filename, 'r', encoding='UTF-8') as f:
    content = f.read()
    lines = content.split("\n")
    loc_results = []
    for ind, line in enumerate(lines):
        if ind % (workers+1) == 0:
            loc_params = [int(x.strip()) for x in line.split(" ")]
            params.append(loc_params)
        else:
            value = float(line.split(',')[-1].strip())
            loc_results.append(value)
    for ind, val in enumerate(loc_results):
        result[(ind % workers)].append(val)

params = [x[4] for x in params]

for i in range(workers):
    plt.plot(params, result[i], marker='o', linestyle='-', label=names2[i])
plt.title(f'Time performance based on broken walls')
plt.xlabel('Number of broken walls')
plt.ylabel(f'Time')
plt.legend()
plt.show()
