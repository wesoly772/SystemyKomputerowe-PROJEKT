from matplotlib import pyplot as plt


def value_label(ax,rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
        xy=(rect.get_x() + rect.get_width() / 2, height),
        xytext=(0, 3),  # przesunięcie tekstu nad słupkiem
        textcoords="offset points",
        ha='center', va='bottom', fontsize=8)

def makegraph_cpu(results,test_index):
    algorithms = list(results.keys())
    turnaround_times = [results[alg][0] for alg in algorithms]
    waiting_times = [results[alg][1] for alg in algorithms]

    #Wykres dla AWT
    fig, ax = plt.subplots(figsize=(8,5))
    rects = ax.bar(algorithms,waiting_times)
    ax.set_title(f"Test {test_index} - Średni czas oczekiwania")
    ax.set_ylabel("Czas oczekiwania")
    max_y = max(waiting_times) * 1.5
    ax.set_ylim(0,max_y)
    value_label(ax,rects)
    plt.tight_layout()
    plt.savefig("avg_waiting.png")
    plt.close()



    #Wykres dla ATT
    fig, ax = plt.subplots(figsize=(8,5))
    rects = ax.bar(algorithms,turnaround_times)
    ax.set_title(f"Test {test_index} - Średni czas realizacji")
    ax.set_ylabel("Czas realizacji")
    max_y = max(waiting_times) * 1.5
    ax.set_ylim(0,max_y)
    value_label(ax,rects)
    plt.tight_layout()
    plt.savefig("avg_turnaround.png")
    plt.close()


def makegraph_page(results,test_index):
    algorithms = list(results.keys())
    faults = [results[alg] for alg in algorithms ]

    fig, ax = plt.subplots(figsize=(8,5))
    rects = ax.bar(algorithms,faults)
    ax.set_title(f"Test {test_index} - Faults ")
    ax.set_ylabel("Faults")
    max_y = max(faults) * 1.5
    ax.set_ylim(0,max_y)
    value_label(ax,rects)
    plt.tight_layout()
    plt.savefig("faults.png")
    plt.close()
    