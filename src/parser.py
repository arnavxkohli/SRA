import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Scheduling Coursework CLI')

    parser.add_argument('-l', '--list_length', type=int, default=20, help='List length for Tabu search')
    parser.add_argument('-m', '--max_iterations', type=int, default=1000, help='Maximum iterations for Tabu search')
    parser.add_argument('-t', '--tolerance', type=int, default=10, help='Tolerance for Tabu search')

    parser.add_argument('-s', '--save_output', action='store_true', help='Save output to files')

    parser.add_argument('-r', '--run', choices=['tabu', 'lcl', 'both'], default='both', help='Select which algorithm to run: tabu, lcl, or both')
    return parser.parse_args()
