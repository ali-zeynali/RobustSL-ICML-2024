import json

from DynamicRSL import *
from DataGenerator import *


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

# ns = [100, 500, 1000, 10000]
ns =  [100, 200, 500, 1000, 2000]

errors = [0, 0.9]
search_size = 100000
alpha = 2
p0_vals = [0.005, 0.01, 0.02, 0.05, 0.1, 0.2]
insert_ratio = 0.2

__generate_data__ = True
__test_samples__ = True

trials = 1
__path_dir__ = "P0Test"
for n in ns:
    for idx, error in enumerate(errors):
        for p0 in p0_vals:

            print("n: {2}, p0: {1}, Evaluating error: {0}".format(error, p0, n))

            if __generate_data__:
                if error == 0:
                    key_values, initial_elements, queries, search_frequencies, ranks = generate_dynamic_keys(n,
                                                                                                             search_size,
                                                                                                             alpha,
                                                                                                             __random_order__=False,
                                                                                                             insert_ratio=insert_ratio)

                else:
                    data = read_data("{1}/data_n{2}_e{0}.json".format(0, __path_dir__, n))
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
                write_data(data, "{1}/data_n{2}_e{0}.json".format(int(error * 100), __path_dir__, n))
            else:
                data = read_data("{1}/data_n{2}_e{0}.json".format(int(error * 100), __path_dir__, n))

                key_values = data['keys']
                queries = data['search']
                frequencies = data['freq']
                search_frequencies = data['search_freq']
                ranks = data['ranks']
                initial_elements = data['init_keys']


            print("n: {1}, alpha: {0}, Making RSL...".format(alpha, n))
            rsl = DynamicRSL(initial_elements.copy(), frequencies.copy(), p0=p0, right_comparison=False)

            TestDS(rsl, queries,
                   "{2}/RSL_n{3}_e{0}_p{1}.json".format(int(error * 100), p0, __path_dir__, n))

            print("n: {1}, alpha: {0}, Making RSL+...".format(alpha, n))
            rsl = DynamicRSL(initial_elements.copy(), frequencies.copy(), p0=p0, right_comparison=True)

            TestDS(rsl, queries,
                   "{2}/RSLP_n{3}_e{0}_p{1}.json".format(int(error * 100), p0, __path_dir__, n))



