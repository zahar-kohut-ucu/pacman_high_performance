import matplotlib.pyplot as plt

data = [0,0]
labels = ['Djikstra', 'A-star']

with open('./results/res_game_perf.txt', 'r') as f:
    for line in f:
        line = line.split(", ")
        if len(line) == 3:
            if int(line[0]) > int(line[1]):
                data[0] += 1
            elif int(line[0]) < int(line[1]):
                data[1] += 1        


def plot_pie_chart(data, labels):
    plt.pie(data, labels=labels, autopct='%1.1f%%')
    plt.show()
    
plot_pie_chart(data, labels)