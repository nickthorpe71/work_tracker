import argparse
from search import binary, depth_first, breadth_first


def main():
    parser = argparse.ArgumentParser(description="Search for word in file")

    # word
    parser.add_argument('-w', '--word', required=True,
                        help="Word to search for")

    # file
    parser.add_argument('-f', '--file', required=True,
                        help="Path to the file that is to be searched")

    # search algorithm
    parser.add_argument('-sa', '--search-algorithm', choices=[
                        "binary-search", "depth-first-search", "breadth-first-search"], required=True, help="The algorithm to use for searching")

    # tree traversal order
    parser.add_argument('-o', '--order', choices=[
        "pre-order", "post-order", "in-order", "level-order"], required=True, help="The order in which to traverse the tree")

    args = parser.parse_args()

    # routes
    if args.search_algorithm == "depth-first-search":
        depth_first.search(args)
        return

    if args.search_algorithm == "breadth-first-search":
        breadth_first.search(args)
        return

    if args.search_algorithm == "binary-search":
        binary.search(args)
        return


if __name__ == '__main__':
    main()
