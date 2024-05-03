from BinaryTree import *
from SkipListNode import *


class BTSkipList(DS):
    def __init__(self, ordered_elements, frequencies, binary_trees=[None, None], alpha=1):
        DS.__init__(self)
        self.n = len(ordered_elements)
        self.elements = ordered_elements
        self.frequencies = frequencies
        self.binary_trees = binary_trees
        self.first_node, self.height = self.make_skip_list(ordered_elements, frequencies, binary_trees=binary_trees,
                                                           alpha=alpha)

    def make_skip_list(self, ordered_elements, frequencies, binary_trees=[None, None], alpha=1):
        if binary_trees[0] is None:
            pessimistic_tree = BinaryTree(ordered_elements, frequencies=frequencies, pessimistic=True).BFS()
        else:
            pessimistic_tree = binary_trees[0].BFS()
        if binary_trees[1] is None:
            optimistic_tree = BinaryTree(ordered_elements, frequencies=frequencies, pessimistic=False).BFS()
        else:
            optimistic_tree = binary_trees[1].BFS()

        balanced_tree = [[] for _ in range(int(alpha * len(pessimistic_tree)))]
        for i in range(len(pessimistic_tree)):
            balanced_tree[max(int(alpha*(i+1)) - 1, i)] = pessimistic_tree[i]



        node1 = SkipListNode(float('-inf'))
        node2 = SkipListNode(float('inf'))
        node1.right = node2
        node2.left = node1

        node1.generate_down()
        node2.generate_down()
        previous_nodes = [node1, node2]
        h = 0
        while len(previous_nodes) < self.n + 2:
            balanced = balanced_tree[h]
            optimistic = optimistic_tree[h]
            nodes = []
            i = 0
            j = 0
            k = 0
            while i < len(balanced) or j < len(optimistic) or k < len(previous_nodes):
                balance_value = balanced[i].value if i < len(balanced) else float('inf')
                optimistic_value = optimistic[j].value if j < len(optimistic) else float('inf')
                previous_value = previous_nodes[k].value

                min_val = np.min([balance_value, optimistic_value, previous_value])
                if min_val == previous_value:
                    node = previous_nodes[k].down
                else:
                    node = SkipListNode(min_val)
                if len(nodes) > 0:
                    nodes[-1].right = node
                    node.left = nodes[-1]
                nodes.append(node)

                if balance_value == min_val:
                    i += 1
                if optimistic_value == min_val:
                    j += 1
                if previous_value == min_val:
                    k += 1
            for node in nodes:
                if len(nodes) < self.n + 2:
                    node.generate_down()
            previous_nodes = nodes
            h += 1
        return node1.down, h

    def insert(self, key, freq):
        if key not in self.elements:
            self.binary_trees[0].insert(key, freq)
            self.binary_trees[1].insert(key, freq)
            self.elements.append(key)
            self.frequencies = list(self.frequencies)
            self.frequencies.append(freq)
            self.frequencies = np.array(self.frequencies) / np.sum(self.frequencies)
            self.make_skip_list(self.elements, self.frequencies, self.binary_trees)

    def delete(self, key):
        if key in self.elements:
            idx = self.elements.index(key)
            self.elements.remove(key)
            self.frequencies = list(self.frequencies)
            self.frequencies.pop(idx)
            self.frequencies = np.array(self.frequencies) / np.sum(self.frequencies)
            self.binary_trees[0].delete(key)
            self.binary_trees[1].delete(key)
            self.make_skip_list(self.elements, self.frequencies, self.binary_trees)

    def search(self, key_Value, __splay_cost__=False):
        cost = 0
        node = self.first_node
        upper_bound = float('inf')
        while True:
            if node is None:
                return None, cost
            if node.value == key_Value:
                return node, cost
            if node.right.value <= key_Value:
                node = node.right
                cost += 1
                continue
            else:
                if node.right.value < upper_bound:
                    cost += 1
                    upper_bound = min(node.right.value, upper_bound)
                node = node.down

    def BFS(self, __print__=False):
        first_node = self.first_node
        levels = []
        for i in range(self.height):
            node = first_node
            level = []
            while node is not None:
                if __print__:
                    print("\t[ {0} ]".format(node.value), end="")
                level.append(node)
                node = node.right
            levels.append(level)
            first_node = first_node.down
            if __print__:
                print("")
        return levels
