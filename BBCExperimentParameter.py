import json

from DataGenerator import *
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

trials = 20
__path_dir__ = "BBCExperimentParameter"
categories = ['business', 'entertainment', 'politics', 'sport', 'tech']
category = "entertainment"
parameter_values = [0.1 , 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

train_size = int(0.4 * 410)

__do_test__ = True

for p0 in parameter_values:
    print("Analyzing P0 of: {0}".format(p0))
    for trial in range(trials):
        print("Analyzing Trial: {0}".format(trial))
        data_path = "dataset\\bbc\\{0}\\".format(category)
        key_values, search_elements, frequencies, search_frequencies = get_bbc_dataset_adversary(data_path,
                                                                                                 dictionary_size=5500,
                                                                                                 scale_factor=1,
                                                                                                 adversary_ratio=0.25,
                                                                                                 train_size=train_size,
                                                                                                 shuffle=True,
                                                                                                 __print__=True)
        print("Number of keys: {0}, number of search queries: {1}".format(len(key_values), len(search_elements)))

        if __do_test__:

            print("Making RSL...")
            rsl = DynamicRSL(key_values.copy(), frequencies.copy(), p0=p0, right_comparison=False)

            TestDS(rsl, key_values, search_elements,
                   "{1}/RSL_p{0}_t{2}.json".format(p0, __path_dir__, trial))

            print("Making RSL+...")
            rsl = DynamicRSL(key_values.copy(), frequencies.copy(), p0=p0, right_comparison=True)

            TestDS(rsl, key_values, search_elements,
                   "{1}/RSLP_p{0}_t{2}.json".format(p0, __path_dir__, trial))


