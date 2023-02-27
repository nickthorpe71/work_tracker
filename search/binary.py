from data_structures.binary_tree import BinaryTree


def binary_search(word, node):
    if node is None:
        return False

    if node.data == word:
        return True

    if int(node.data) < int(word):
        return binary_search(word, node.right)

    if int(node.data) > int(word):
        return binary_search(word, node.left)


def search(args):
    bst = BinaryTree()

    print("Creating BST from file...")
    bst.create_bst_from_file(args.file)
    print("BST created")

    print("Searching for word...")
    print("Word found" if binary_search(
        args.word, bst.root) else "Word not found")
