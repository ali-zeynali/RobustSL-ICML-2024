import json

from AVLTree import *
from BTSkipList import *
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


__test_samples__ = True

trials = 10
__path_dir__ = "BBCExperimentNoisy"
categories = ['business', 'entertainment']
train_sizes = [5, 10, 50, 100, 200, 500]
adversary_ratios = [0, 0.25, 0.5, 0.75, 0.9]
train_size = int(410*0.4)
__do_test__ = True

for category in categories[1:]:
    print("Analyzing category of: {0}".format(category))
    for adv_size in adversary_ratios:
        print("Analyzing train size: {0}".format(adv_size))
        data_path = "dataset\\bbc\\{0}\\".format(category)
        key_values, search_elements, frequencies, search_frequencies = get_bbc_dataset_adversary(data_path,
                                                                                                 dictionary_size=5500,
                                                                                                 scale_factor=1,
                                                                                                 adversary_ratio=adv_size,
                                                                                                 train_size=train_size,
                                                                                                 shuffle=True)
        print("Number of keys: {0}, number of search queries: {1}".format(len(key_values), len(search_elements)))

        if __do_test__:
            print(" Making balanced BST...")
            balanced_tree = BinaryTree(key_values, pessimistic=True)

            TestDS(balanced_tree, key_values, search_elements,
                   "{1}/BalBST_c{0}_t{2}.json".format(category, __path_dir__, adv_size))


            print("Making RSL...")
            p0 = min(0.9, max(search_frequencies) * 0.9)
            rsl = DynamicRSL(key_values.copy(), frequencies.copy(), p0=p0, right_comparison=False)

            TestDS(rsl, key_values, search_elements,
                   "{1}/RSL_c{0}_t{2}.json".format(category, __path_dir__, adv_size))

            print("Making RSL+...")
            p0 = min(0.9, max(search_frequencies) * 0.9)
            rsl = DynamicRSL(key_values.copy(), frequencies.copy(), p0=p0, right_comparison=True)

            TestDS(rsl, key_values, search_elements,
                   "{1}/RSLP_c{0}_t{2}.json".format(category, __path_dir__, adv_size))

            print("Making Treap...")
            treap = Treap(key_values, frequencies=frequencies)

            TestDS(treap, key_values, search_elements,
                   "{1}/Treap_c{0}_t{2}.json".format(category, __path_dir__, adv_size))
            #


            print("Making AVL Tree...")
            avl = AVLTree(key_values)

            TestDS(avl, key_values, search_elements,
                   "{1}/AVL_c{0}_t{2}.json".format(category, __path_dir__, adv_size))

            print("Making RedBlack Tree...")
            redblack = RedBlackTree(key_values)

            TestDS(redblack, key_values, search_elements,
                   "{1}/RedBlack_c{0}_t{2}.json".format(category, __path_dir__, adv_size))

            print("Making Splay Tree...")
            splay = SplayTree(elements=key_values)

            TestDS(splay, key_values, search_elements,
                   "{1}/Splay_c{0}_t{2}.json".format(category, __path_dir__, adv_size),
                   true_search=True,
                   __splay_cost__=False)

            print("Making Splay Tree+...")
            splayP = SplayTree(elements=key_values)

            TestDS(splayP, key_values, search_elements,
                   "{1}/SplayP_c{0}_t{2}.json".format(category, __path_dir__, adv_size),
                   true_search=True,
                   __splay_cost__=True)
