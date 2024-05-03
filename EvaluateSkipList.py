from matplotlib import pyplot as plt

from BTSkipList import *
from BinaryTree import *
from DataGenerator import *


def plot_CDF(values, path_to_save, x_label):
    sorted_values = sorted(values)
    n = len(values)
    x = []
    y = []
    for i in range(n):
        x.append(sorted_values[i])
        y.append((i + 1) / n)

    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel("CDF")
    plt.savefig(path_to_save, dpi=600)


def plot_n_CDF(values, path_to_save, labels, x_label, title, fig_num):
    plt.figure(fig_num)
    averages = []
    max_x = 0
    for k, value in enumerate(values):
        sorted_values = sorted(value)
        n = len(value)
        x = []
        y = []
        for i in range(n):
            x.append(sorted_values[i])
            y.append((i + 1) / n)
        if sorted_values[-1] > max_x:
            max_x = sorted_values[-1]
        averages.append(np.average(sorted_values))

        plt.plot(x, y, label=labels[k])
    for k in range(len(values)):
        plt.text(max_x - 7, k * 0.1 + 0.3, "Avg({0})= {1:.2f}".format(labels[k], averages[k]))
    plt.xlabel(x_label)
    plt.ylabel("CDF")
    plt.title(title)
    plt.legend()
    plt.savefig(path_to_save, dpi=600)


n = 1000
errors = [0, 0.5, 1, 2, 5, 10]
search_size = 100000
alpha = 2
for fig_num, error in enumerate(errors):
    print("Evaluating error: {0}".format(error))
    key_values, search_elements, frequencies, search_frequencies = zipfi(n, search_size, error, alpha)

    print("Making optimal tree...")
    optimal_tree = BinaryTree(key_values, frequencies, pessimistic=False)
    print("Making balanced tree...")
    balanced_tree = BinaryTree(key_values, pessimistic=True)

    print("Making SkipList...")
    skipList = BTSkipList(key_values, frequencies, binary_trees=[balanced_tree, optimal_tree])

    print("Searching ...")

    all_costs_optimistic = optimal_tree.get_all_costs(key_values)
    costs_optimistic = []
    for key in search_elements:
        costs_optimistic.append(all_costs_optimistic[key])

    all_costs_pessimistic = balanced_tree.get_all_costs(key_values)
    costs_pessimistic = []
    for key in search_elements:
        costs_pessimistic.append(all_costs_pessimistic[key])

    all_costs_skipList = skipList.get_all_costs(key_values)
    costs_BTSkip = []
    for key in search_elements:
        costs_BTSkip.append(all_costs_skipList[key])

    # plot_CDF(costs, "figures/cost_CDF.png", "Value")
    plot_n_CDF([costs_optimistic, costs_pessimistic, costs_BTSkip],
               "figures/zipfi_cost_CDF_e{0}.png".format(int(error * 100)), ["Optimistic", "Pessimistic", "BT-SkipList"],
               "Cost of a Search", "Error = {0}%".format(int(error * 100)), fig_num)
