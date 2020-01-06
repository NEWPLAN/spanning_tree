import heapq
import sys
import numpy as np
node_nums = int(input("Enter value for n:"))  # input n for number of vertices
connection_map = [[x for x in range(node_nums)] for y in range(node_nums)]
# connection_map = [[1, 2, 3, 4], [2, 3, 4, 5], [0, 1, 3, 6], [0, 1, 2, 7],
#                   [0, 5, 6, 7], [1, 4, 6, 7], [2, 4, 5, 7], [3, 4, 5, 6]
#                   ]
print(connection_map)

for each in range(len(connection_map)):
    connection_map[each].remove(each)
# connection_map = [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]

connection_map = np.array(connection_map)


print(connection_map)


class Graph(object):
    def __init__(self, mat):
        self._mat = mat
        self._edge = []
        self._node_num = len(mat)
        self._tree = []
        self._visiable_node = []
        self.collecting_edges()
        self._count = 1
        self._previous = [x for x in range(self._node_num)]
        self._reduce_tree = []

    def collecting_edges(self):
        for src in range(len(self._mat)):
            for dst in self._mat[src]:
                _src = min(src, dst)
                _dst = max(src, dst)
                if [_src, _dst] not in self._edge:
                    self._edge.append([_src, _dst])
        print("edge: ", self._edge)

    def get_root_node(self, index):
        cur_index = index
        while self._previous[cur_index] != cur_index:
            cur_index = self._previous[cur_index]
        return cur_index

    def DFS_search(self, index=0):
        if index >= len(self._edge):
            # print("return, in the end")
            return
        # self.show_all()
        current_edge = self._edge[index]
        root_a = self.get_root_node(current_edge[0])
        root_b = self.get_root_node(current_edge[1])
        root_current_edge = self._previous[current_edge[1]]
        if root_a != root_b:  # current edge is the exact one expected, merge into one.
            self._tree.append(current_edge)
            if self.generate_final_tree():  # come to the end, and reverse
                # print("search for the next, ", self._tree)
                self._tree.pop()
                self.DFS_search(index + 1)
                return
            else:  # search the next nodes
                self._previous[root_b] = self._previous[root_a]
                self.DFS_search(index + 1)
                self._previous[current_edge[1]] = root_current_edge
                self._previous[root_b] = root_b
                self._tree.pop()
                self.DFS_search(index + 1)
        else:  #
            self.DFS_search(index + 1)

    def generate_final_tree(self):
        if len(self._tree) == self._node_num - 1:  # generated a tree
            # print("Tree {}: ".format(self._count), end='')
            self._reduce_tree.append(self._tree.copy())
            self._count += 1
            # print(self._tree)
            return True
        return False

    def show_all(self):
        print("Show all ")
        print(self._tree)
        print(self._visiable_node)


a_graph = Graph(connection_map)
a_graph.DFS_search()


def generate_tree_cost(tree, root_id=0, node_nums=4):
    tree_mat = [[0 for x in range(node_nums)]
                for y in range(node_nums)]
    for each_link in tree:
        tree_mat[each_link[0]][each_link[1]] = 1
        tree_mat[each_link[1]][each_link[0]] = 1

    #root_id = 0
    cost_node = {}
    visited = [root_id]
    layer = 1
    cost_node[root_id] = 0

    while len(visited) != 0:
        tmp_vis = []
        for each in visited:
            root_link = tree_mat[each]
            #print(each, root_link, cost_node, visited)
            for dst in range(node_nums):
                if root_link[dst] == 1:
                    #print("DST: ", dst)
                    if dst not in cost_node:
                        cost_node[dst] = layer
                        tmp_vis.append(dst)
        visited = tmp_vis
        layer += 1
    return cost_node


for each_tree in a_graph._reduce_tree:
    tree_cost = generate_tree_cost(
        each_tree, root_id=1, node_nums=a_graph._node_num)
    print(each_tree, " ----> ", tree_cost)
print(len(a_graph._reduce_tree))
# tree_cost = generate_tree_cost(
#     [[0, 4], [1, 2], [1, 3], [2, 4]], root_id=1, node_nums=5)
# print([[0, 4], [1, 2], [1, 3], [2, 4]], " ----> ", tree_cost)
