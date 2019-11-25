
class PriorityQueue:

    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.lookup = [-1] * self.get_capacity()
        self.elems = [None] * (self.get_capacity() + 1)

    def get_capacity(self):
        return self.capacity

    def get_size(self):
        return self.size

    def is_empty(self):
        return self.get_size() == 0

    def insert(self, node):
        self.size += 1
        self.elems[self.size] = node
        self.lookup[node.get_id()] = self.size

        index = self.size
        while True:
            if index == 1:
                break

            p_index = self.get_parent_index(index)
            p_node = self.elems[p_index]
            if node.get_cost() >= p_node.get_cost():
                break

            self.swap_nodes(index, p_index)
            index = p_index

    def decrease_key(self, node):
        c_index = self.lookup[node.get_id()]
        c_key = node.get_cost()
        if c_index == 1:
            return

        p_index = self.get_parent_index(c_index)
        p_key = self.elems[p_index].get_cost()
        if p_key <= c_key:
            return

        self.swap_nodes(c_index, p_index)
        self.decrease_key(self.elems[p_index])

    def delete_min(self):
        result = self.elems[1]

        self.swap_nodes(self.size, 1)
        self.elems[self.size] = None
        self.size -= 1
        if self.get_size() == 0:
            return result

        node = self.elems[1]
        while True:
            index = self.lookup[node.get_id()]
            if self.is_leaf_node(index):
                break

            l_index = self.get_left_child_index(index)
            r_index = self.get_right_child_index(index)

            l_node = self.elems[l_index]
            r_node = self.elems[r_index]
            p_node = self.elems[index]

            p_key = p_node.get_cost()
            l_key = l_node.get_cost()
            r_key = None if r_node == None else r_node.get_cost()
            if p_key <= l_key and (r_key == None or p_key <= r_key):
                break

            s_index = l_index if r_key == None or l_key < r_key else r_index
            self.swap_nodes(index, s_index)
            node = self.elems[s_index]

        return result

    def is_leaf_node(self, index):
        l = self.get_left_child_index(index)
        r = self.get_right_child_index(index)
        return l > self.get_size() and r > self.get_size()

    def get_parent_index(self, index):
        return index // 2

    def get_left_child_index(self, index):
        return 2 * index

    def get_right_child_index(self, index):
        return 2 * index + 1

    def swap_nodes(self, index_a, index_b):
        elem_a = self.elems[index_a]
        elem_b = self.elems[index_b]

        self.elems[index_a] = elem_b
        self.elems[index_b] = elem_a

        self.lookup[elem_a.get_id()] = index_b
        self.lookup[elem_b.get_id()] = index_a

    def print(self, label='PriortyQueue'):
        print('{}: {}/{}'.format(label, self.get_size(), self.get_capacity()))
        print('elements: {}'.format(self.elems))
        print('lookup:   {}'.format(self.lookup))
        print('')
