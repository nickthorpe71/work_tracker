import argparse
# from search.search_setup import file_search_setup
from work_intervals.main import setup_works_intervals

def main():
    parser = argparse.ArgumentParser(description="Useful toolz")
    
    setup_works_intervals(parser)
    # file_search_setup(parser)
    
if __name__ == '__main__':
    main()
