import json

from AVLTree import *
from DataGenerator import *
from DynamicRSL import *
from RedBlackTree import *
from SplayTree import *
from Treap import *


def TestDS(ds, search_queries, path_to_save, __splay_cost__=False,
           __print__=False, _skip_delete_=False, overWrite=False):
    search_costs = []

    for query in search_queries:
        if not overWrite:
            query_type = query['type']
            if query_type == "search":
                n, c = ds.search(query['key'], __splay_cost__=__splay_cost__)
                search_costs.append(c)
            elif query_type == "insert":
                ds.insert(query['key'], query['freq'])
            elif query_type == "delete" and not _skip_delete_:
                ds.delete(query['key'])
        else:
            query_type = query['type']
            if query_type == "search":
                search_costs.append(0)

    write_data(search_costs, path_to_save)
    return search_costs

def copyResult(base_path, new_path):
    data = read_data(base_path)
    write_data(data, new_path)



def write_data(data, path_to_save):
    with open(path_to_save, 'w') as writer:
        json.dump(data, writer)


def read_data(path):
    with open(path) as reader:
        return json.load(reader)

ns = [100, 500, 1000, 2000]

errors = [0, 0.01,  0.45, 0.9]

search_size = 100000
alpha = 2
insert_ratio = 0.2

__generate_data__ = False
__test_samples__ = True

trials = 1
__path_dir__ = "AdvOrderDynamic"
for n in ns:
    for trial in range(0, trials):
        for idx, error in enumerate(errors):
            print("n: {2}, Trial: {1}, Evaluating error: {0}".format(error, trial, n))

            if __generate_data__:
                if error == 0 and trial == 0:
                    key_values, initial_elements, queries, search_frequencies, ranks = generate_dynamic_keys(n,
                                                                                                             search_size,
                                                                                                             alpha,
                                                                                                             __random_order__=False,
                                                                                                             insert_ratio=insert_ratio)

                else:
                    data = read_data("{2}/data_n{3}_e{0}_t{1}.json".format(0, 0, __path_dir__, n))
                    key_values = data['keys']
                    initial_elements = data['init_keys']
                    queries = data['search']
                    ranks = data['ranks']
                    search_frequencies = data['search_freq']

                queries, frequencies = zipfi_dynamic_fixed(n, key_values, initial_elements, ranks, queries, error, alpha)
                data = {}
                data['keys'] = key_values
                data['search'] = queries
                data['freq'] = frequencies
                data['search_freq'] = search_frequencies
                data['init_keys'] = initial_elements
                data['ranks'] = ranks
                write_data(data, "{2}/data_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))
            else:
                data = read_data("{2}/data_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))

                key_values = data['keys']
                queries = data['search']
                frequencies = data['freq']
                search_frequencies = data['search_freq']
                ranks = data['ranks']
                initial_elements = data['init_keys']



            ###################################################




            print("n: {1}, Trial: {0}, Making Splay Tree...".format(trial, n))
            splay = SplayTree(elements=initial_elements.copy())

            TestDS(splay, queries,
                   "{2}/Splay_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n),
                   __splay_cost__=False)
            #
            print("n: {1}, Trial: {0}, Making Splay Tree+...".format(trial, n))
            splayP = SplayTree(elements=initial_elements.copy())

            TestDS(splayP, queries,
                   "{2}/SplayP_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n),
                   __splay_cost__=True)

            print("n: {1}, Trial: {0}, Making Treap...".format(trial, n))
            if n <= 10000:
                treap = Treap(initial_elements.copy(), frequencies=frequencies.copy())

                TestDS(treap, queries,
                       "{2}/Treap_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))
            else:
                TestDS(None, queries,
                       "{2}/Treap_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n), overWrite=True)

            print("n: {1}, Trial: {0}, Making LA-BTree...".format(trial, n))
            if n <= 10000:
                treap = Treap(initial_elements.copy(), frequencies=frequencies.copy(), log_priority=True)

                TestDS(treap, queries,
                       "{2}/LABTree_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))
            else:
                TestDS(None, queries,
                       "{2}/LABTree_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n), overWrite=True)



            print("n: {1}, Trial: {0}, Making RSL...".format(trial, n))
            p0 = 0.05
            rsl = DynamicRSL(initial_elements.copy(), frequencies.copy(), p0=p0, right_comparison=False)

            TestDS(rsl, queries,
                   "{2}/RSL_n{3}_e{0}_t{1}_P0.json".format(int(error * 100), trial, __path_dir__, n))

            print("n: {1}, Trial: {0}, Making RSL+...".format(trial, n))
            p0 = 0.05
            rsl = DynamicRSL(initial_elements.copy(), frequencies.copy(), p0=p0, right_comparison=True)

            TestDS(rsl, queries,
                   "{2}/RSLP_n{3}_e{0}_t{1}_P0.json".format(int(error * 100), trial, __path_dir__, n))

            if error == 0 and trial == 0:

                print("n: {1}, Trial: {0}, Making balanced BST...".format(trial, n))
                balanced_tree = BinaryTree(initial_elements.copy(), frequencies=frequencies.copy(), pessimistic=True)

                TestDS(balanced_tree, queries,
                       "{2}/BalBST_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))

                print("n: {1}, Trial: {0}, Making AVL Tree...".format(trial, n))
                avl = AVLTree(initial_elements.copy())

                TestDS(avl, queries,
                       "{2}/AVL_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))

                print("n: {1}, Trial: {0}, Making RedBlack Tree...".format(trial, n))
                redblack = RedBlackTree(initial_elements.copy())

                TestDS(redblack, queries,
                       "{2}/RedBlack_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n),
                       _skip_delete_=True)
            else:
                print("n: {1}, Trial: {0}, Making balanced BST...".format(trial, n))
                copyResult("{2}/BalBST_n{3}_e{0}_t{1}.json".format(int(0 * 100), 0, __path_dir__, n),
                           "{2}/BalBST_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))

                print("n: {1}, Trial: {0}, Making AVL Tree...".format(trial, n))
                copyResult("{2}/AVL_n{3}_e{0}_t{1}.json".format(int(0 * 100), 0, __path_dir__, n),
                           "{2}/AVL_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))

                print("n: {1}, Trial: {0}, Making RedBlack Tree...".format(trial, n))
                copyResult("{2}/RedBlack_n{3}_e{0}_t{1}.json".format(int(0 * 100), 0, __path_dir__, n),
                           "{2}/RedBlack_n{3}_e{0}_t{1}.json".format(int(error * 100), trial, __path_dir__, n))




