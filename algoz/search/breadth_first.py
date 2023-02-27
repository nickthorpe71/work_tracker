from data_structures.binary_tree import BinaryTree


def search(args):
    bt = BinaryTree()
    bt.create_from_file(args.file)

    if not args.order == "level-order":
        print("Sorry, only level order traversal is supported for breadth first search")
        return

    print("Found word!" if bfs(bt.root, args.word) else "Word not found")


def bfs(node, target):
    if node.data == target:
        return True
    if node.left:
        if bfs(node.left, target):
            return True
    if node.right:
        if bfs(node.right, target):
            return True
    return False
