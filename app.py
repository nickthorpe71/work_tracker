import argparse
from search import search_setup


def main():
    parser = argparse.ArgumentParser(description="Useful toolz")
    search_setup(parser)
    


if __name__ == '__main__':
    main()
