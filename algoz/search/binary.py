from data_structures.binary_tree import BinaryTree
from data_structures.queue import Queue


def search(args):
    bst = BinaryTree()

    print("Creating BST from file...")
    bst.create_bst_from_file(args.file)
    print("BST created")

    bst.in_order_print(bst.root)
