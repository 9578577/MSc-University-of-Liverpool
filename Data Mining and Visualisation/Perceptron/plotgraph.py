import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def perceptron_accuracy(accuracy_per_epoch, class_remove, number_classes, type):
    classes = [(i+1) for i in range(number_classes)]
    classes = [y for y in classes if y != int(class_remove)]
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.plot(range(len(accuracy_per_epoch)), accuracy_per_epoch, label=(str(classes[0]) + " vs " + str(classes[1])))
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend(loc="lower right", prop={'size': 10})
    if type == "train":
        plt.savefig("charts/train_" + str(classes[0]) + " vs " + str(classes[1]))
    else:
        plt.savefig("charts/test_" + str(classes[0]) + " vs " + str(classes[1]))
    plt.show()
    return

def multiperceptron_accuracy(accuracy_per_epoch, type):
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    for i in range(len(accuracy_per_epoch)):
        plt.plot(range(len(accuracy_per_epoch[i])), accuracy_per_epoch[i], label="Class " + str(i+1))
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend(loc="lower right", prop={'size': 10})
    if type == "train":
        plt.savefig("charts/train_multiperceptron.png")
    else:
        plt.savefig("charts/test_multiperceptron.png")
    plt.show()
    return

def l2_multiperceptron_accuracy(accuracy_per_epoch, lam, type):
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    for i in range(len(accuracy_per_epoch)):
        plt.plot(range(len(accuracy_per_epoch[i])), accuracy_per_epoch[i], label="Class " + str(i+1))
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend(loc="lower right", prop={'size': 10})
    if type == "train":
        plt.savefig("charts/train_" + str(lam) + "_l2_multiperceptron.png")
    else:
        plt.savefig("charts/test_" + str(lam) + "_l2_multiperceptron.png")
    plt.show()
    return