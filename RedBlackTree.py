import sys

from BTNode import *
from DS import *


class RedBlackTree(DS):
    def __init__(self, elements=[]):
        DS.__init__(self)
        self.TNULL = BTNode(-1)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL
        self.elements = []
        if len(elements) > 0:
            for v in elements:
                self.insert(v, None)


    # Search the tree
    def search_tree_helper(self, node, key):
        if node == self.TNULL or key == node.value:
            return node, 1

        if key < node.value:
            n, c = self.search_tree_helper(node.left, key)

        else:
            n, c = self.search_tree_helper(node.right, key)
        return n, c + 1

    # Balancing the tree after deletion
    def delete_fix(self, x):
        try:
            while x != self.root and x.color == 0:
                if x == x.parent.left:
                    s = x.parent.right
                    if s.color == 1:
                        s.color = 0
                        x.parent.color = 1
                        self.left_rotate(x.parent)
                        s = x.parent.right

                    if s.left.color == 0 and s.right.color == 0:
                        s.color = 1
                        x = x.parent
                    else:
                        if s.right.color == 0:
                            s.left.color = 0
                            s.color = 1
                            self.right_rotate(s)
                            s = x.parent.right

                        s.color = x.parent.color
                        x.parent.color = 0
                        s.right.color = 0
                        self.left_rotate(x.parent)
                        x = self.root
                else:
                    s = x.parent.left
                    if s.color == 1:
                        s.color = 0
                        x.parent.color = 1
                        self.right_rotate(x.parent)
                        s = x.parent.left

                    if s.right.color == 0 and s.right.color == 0:
                        s.color = 1
                        x = x.parent
                    else:
                        if s.left.color == 0:
                            s.right.color = 0
                            s.color = 1
                            self.left_rotate(s)
                            s = x.parent.left

                        s.color = x.parent.color
                        x.parent.color = 0
                        s.left.color = 0
                        self.right_rotate(x.parent)
                        x = self.root
            x.color = 0
        except Exception as e:
            print("Exception happened in RedBlack Tree!")
            exit(-1)

    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Node deletion
    def delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.value == key:
                z = node

            if node.value <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("Cannot find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right == self.TNULL):
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.delete_fix(x)

    # Balance the tree after insertion
    def fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    # Printing the tree
    def __print_helper(self, node, indent, last):
        if node != self.TNULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.value) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)


    def search(self, k, __splay_cost__=False):
        return self.search_tree_helper(self.root, k)

    def insert(self, key, freq):
        if key in self.elements:
            log = "inserting {0} failed. N = {1}".format(key, len(self.elements))
            with open("RandomOrderDynamic/log.txt", 'a') as writer:
                writer.write(log + "\n")
            return
        else:
            log = "{0} inserted. N = {1}".format(key, len(self.elements))
            with open("RandomOrderDynamic/log.txt", 'a') as writer:
                writer.write(log + "\n")
            self.elements.append(key)
        node = BTNode(key)
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.value < x.value:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.value < y.value:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        self.fix_insert(node)

    def delete(self, key):
        if key not in self.elements:
            log = "{0} deletion failed. N = {1}".format(key, len(self.elements))
        else:
            log = "{0} deleted. N= {1}".format(key, len(self.elements))
            self.elements.remove(key)
            self.delete_node_helper(self.root, key)

        with open("RandomOrderDynamic/log.txt", 'a') as writer:
            writer.write(log+ "\n")


    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    def successor(self, x):
        if x.right != self.TNULL:
            return self.minimum(x.right)

        y = x.parent
        while y != self.TNULL and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self, x):
        if (x.left != self.TNULL):
            return self.maximum(x.left)

        y = x.parent
        while y != self.TNULL and x == y.left:
            x = y
            y = y.parent

        return y

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y


    def get_root(self):
        return self.root


    def print_tree(self):
        self.__print_helper(self.root, "", True)
