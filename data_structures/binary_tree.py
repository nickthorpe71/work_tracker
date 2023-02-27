from data_structures.node import Node
from data_structures.queue import Queue


class BinaryTree:
    def __init__(self):
        self.root = None

    def level_roder_insert(self, data):
        if self.root is None:
            self.root = Node(data)
            return

        queue = Queue()
        queue.enqueue(self.root)

        while queue.get_len() > 0:
            node = queue.dequeue()

            if not node.left:
                node.left = Node(data)
                return
            else:
                queue.enqueue(node.left)

            if not node.right:
                node.right = Node(data)
                return
            else:
                queue.enqueue(node.right)

    def bst_insert_recursive(self, data, node):
        if int(data) < int(node.data):
            if node.left is None:
                node.left = Node(data)
            else:
                self.bst_insert_recursive(data, node.left)

        if int(data) > int(node.data):
            if node.right is None:
                node.right = Node(data)
            else:
                self.bst_insert_recursive(data, node.right)

    def bst_insert(self, data):
        if self.root is None:
            self.root = Node(data)
            return

        self.bst_insert_recursive(data, self.root)

    def create_from_file(self, path):
        with open(path, 'r') as a_file:
            for line in a_file:
                stripped_line = line.strip()
                if stripped_line == "":
                    continue

                words = stripped_line.split()
                for word in words:
                    self.level_roder_insert(word)

    def create_bst_from_file(self, path):
        with open(path, 'r') as a_file:
            for line in a_file:
                stripped_line = line.strip()
                if stripped_line == "":
                    continue

                words = stripped_line.split()
                for word in words:
                    self.bst_insert(word)

    def in_order_print(self, node):
        if node is None:
            return

        self.in_order_print(node.left)
        print(node.data)
        self.in_order_print(node.right)
