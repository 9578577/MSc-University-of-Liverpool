import matplotlib.pyplot as plt

def plot(data, legends, k, title, distance_measure, filename):
    if not len(data) == len(legends):
        print("There must be one legend per dataset")
        return

    fig = plt.plot()
    
    # Plot all our datapoints
    for i in range(len(data)):
        if(legends[i] == "Min") or (legends[i] == "Max"):
            plt.plot([j+1 for j in range(k)], data[i], label=legends[i], linestyle="dashed")
        else:
            plt.plot([j+1 for j in range(k)], data[i], label=legends[i])
    
    plt.xlabel("K")
    plt.ylabel("Percentage")
    plt.legend(loc="lower right", prop={'size': 10})
    
    plt.title(title)
    plt.savefig("charts/"+distance_measure+"/"+filename+".png")
    plt.show()

def plot_error(data, legends, SD, k, title, distance_measure, filename):
    if not len(data) == len(legends):
        print("There must be one legend per dataset")
        return

    fig = plt.plot()
    
    # Plot all our datapoints
    for i in range(len(data)):
        if(legends[i] == "Min") or (legends[i] == "Max"):
            plt.plot([j+1 for j in range(k)], data[i], label=legends[i], linestyle="dashed")
        else:
            plt.errorbar([j+1 for j in range(k)], data[i], SD, label=legends[i], capsize=5, elinewidth=1, markeredgewidth=2, ecolor='red', fmt='r', linewidth=1, capthick = 0.5)
    
    plt.xlabel("K")
    plt.ylabel("Percentage")
    plt.legend(loc="lower right", prop={'size': 10})
    
    plt.title(title)
    plt.savefig("charts/"+distance_measure+"/"+filename+".png")
    plt.show()