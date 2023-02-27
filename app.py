import argparse
# from search.search_setup import file_search_setup
from work_intervals.main import log_time

def main():
    parser = argparse.ArgumentParser(description="Useful toolz")
    
    parser.add_argument('-lt', '--log-time', required=False, help="log work time in database")
    logged = parser.parse_args().log_time
    if logged:
        log_time(logged)

    # file_search_setup(parser)
    
if __name__ == '__main__':
    main()
