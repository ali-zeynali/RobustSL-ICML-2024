import json

from AVLTree import *
from DataGenerator import *
from RedBlackTree import *
from SplayTree import *
from Treap import *
from DynamicRSL import *


def TestDS(ds, ordered_elements, search_elements, path_to_save, true_search=False, __splay_cost__=False,
           __print__=False):
    costs = []
    if not true_search:
        all_costs_optimistic = ds.get_all_costs(ordered_elements)
        for key in search_elements:
            costs.append(all_costs_optimistic[key])
    else:
        for key in search_elements:
            n, c = ds.search(key, __splay_cost__=__splay_cost__)
            costs.append(c)

    write_data(costs, path_to_save)
    return costs


def write_data(data, path_to_save):
    with open(path_to_save, 'w') as writer:
        json.dump(data, writer)


def read_data(path):
    with open(path) as reader:
        return json.load(reader)



ns = [100, 200, 500,  1000, 2000]

errors = [0, 0.01,  0.45, 0.9]
errors = [0]
search_size = 100000
alpha = 2
skipLists_alphas = [1]

__generate_data__ = False
__test_samples__ = True

trials = 1
__path_dir__ = "RandomOrder"
for n in ns:
    for trial in range(trials):
        for idx, error in enumerate(errors):
            print("n: {2}, Trial: {1}, Evaluating error: {0}".format(error, trial, n))

            if __generate_data__:
                if error == 0 and trial == 0:
                    key_values, search_elements, search_frequencies, ranks = generate_keys(n, search_size, alpha,
                                                                                           __random_order__=True)
                else:
                    data = read_data("{2}/data_n{3}_e{0}_t{1}.json".format(0, 0, __path_dir__, n))
                    key_values = data['keys']
                    search_elements = data['search']
                    ranks = data['ranks']
                    search_frequencies = data['search_freq']

                frequencies = zipfi_adversary(n, ranks, error, alpha)

                data = {}
                data['keys'] = key_values
                data['search'] = search_elements
                data['freq'] = frequencies
                data['search_freq'] = search_frequencies
                data['ranks'] = ranks
                write_data(data, "{2}/data_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))




            else:
                data = read_data("{2}/data_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))
                key_values = data['keys']
                search_elements = data['search']
                frequencies = data['freq']
                search_frequencies = data['search_freq']



            p0 = 0.05
            rsl = DynamicRSL(key_values.copy(), frequencies.copy(), p0=p0, right_comparison=False)
            print("n: {0}, memory: {1}".format(n, rsl.memory))

            p0 = 0.05
            rsl = DynamicRSL(key_values.copy(), [1/len(key_values) for _ in range(len(key_values))], p0=p0, right_comparison=False)
            print("Single- n: {0}, memory: {1}".format(n, rsl.memory))
            #
            TestDS(rsl, key_values, search_elements,
                   "{2}/RSL_n{3}_e{0}_t{1}_P0.json".format(int(error * 100), trial, __path_dir__, n))

            print("n: {1}, Trial: {0}, Making RobustSLP...".format(trial, n))
            p0 = 0.05
            rsl = DynamicRSL(key_values.copy(), frequencies.copy(), p0=p0, right_comparison=True)

            TestDS(rsl, key_values, search_elements,
                   "{2}/RSLP_n{3}_e{0}_t{1}_P0.json".format(int(error * 100), trial, __path_dir__, n))

            print("n: {1}, Trial: {0}, Making balanced BST...".format(trial, n))
            balanced_tree = BinaryTree(key_values, pessimistic=True)
            #
            # TestDS(balanced_tree, key_values, search_elements,
            #        "{2}/BalBST_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))

            print("n: {1}, Trial: {0}, Making optimal BST...".format(trial, n))
            optimal_tree = BinaryTree(key_values, frequencies=frequencies, pessimistic=False)

            TestDS(optimal_tree, key_values, search_elements,
                   "{2}/OPTBST_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))

            print("n: {1}, Trial: {0}, Making Treap...".format(trial, n))
            treap = Treap(key_values, frequencies=frequencies)

            TestDS(treap, key_values, search_elements,
                   "{2}/Treap_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))



            print("n: {1}, Trial: {0}, Making AVL Tree...".format(trial, n))
            avl = AVLTree(key_values)

            TestDS(avl, key_values, search_elements,
                   "{2}/AVL_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))

            print("n: {1}, Trial: {0}, Making RedBlack Tree...".format(trial, n))
            redblack = RedBlackTree(key_values)

            TestDS(redblack, key_values, search_elements,
                   "{2}/RedBlack_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))

            print("n: {1}, Trial: {0}, Making Splay Tree...".format(trial, n))
            splay = SplayTree(elements=key_values)

            TestDS(splay, key_values, search_elements,
                   "{2}/Splay_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n),
                   true_search=True,
                   __splay_cost__=False)

            print("n: {1}, Trial: {0}, Making Splay Tree+...".format(trial, n))
            splayP = SplayTree(elements=key_values)

            TestDS(splayP, key_values, search_elements,
                   "{2}/SplayP_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n),
                   true_search=True,
                   __splay_cost__=True)
