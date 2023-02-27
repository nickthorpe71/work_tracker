from data_structures.binary_tree import BinaryTree


def pre_order_search(node, word):
    '''
    1. Visit the root
    2. Traverse the left subtree
    3. Traverse the right subtree
    '''

    if node is None:
        return False

    if node.data == word:
        return True

    if pre_order_search(node.left, word):
        return True

    if pre_order_search(node.right, word):
        return True

    return False


def post_order_search(node, word):
    '''
    1. Traverse the left subtree
    2. Traverse the right subtree
    3. Visit the root
    '''

    if node is None:
        return False

    if post_order_search(node.left, word):
        return True

    if post_order_search(node.right, word):
        return True

    if node.data == word:
        return True

    return False


def in_order_search(node, word):
    '''
    1. Traverse the left subtree
    2. Visit the root
    3. Traverse the right subtree
    '''

    if node is None:
        return False

    if in_order_search(node.left, word):
        return True

    if node.data == word:
        return True

    if in_order_search(node.right, word):
        return True

    return False


order_dict = {
    'pre-order': pre_order_search,
    'post-order': post_order_search,
    'in-order': in_order_search
}


def search(args):
    bt = BinaryTree()

    print("Creating tree from file...")
    bt.create_from_file(args.file)
    print("Tree created")

    valid_orders = order_dict.keys()

    if args.order not in valid_orders:
        print(
            f"Sorry, only {', '.join(valid_orders)} traversal methods are supported for depth first search")
        return

    print("Searching tree for word...")
    print("Found word!" if order_dict[args.order](
        bt.root, args.word) else "Word not found")
    return
