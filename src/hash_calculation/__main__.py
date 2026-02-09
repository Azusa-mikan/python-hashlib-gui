import sys

from hash_calculation.core import args, run_calculate, get_file_name
from hash_calculation.gui import select_algorithm, select_file, input_hash
from hash_calculation.tui import select_algorithm as tui_select_algorithm
from hash_calculation.tui import select_file as tui_select_file
from hash_calculation.tui import input_hash as tui_input_hash

def main():
    tui_mode = False
    if len(sys.argv) > 1:
        tui_mode, file_path, algorithm, compare_hash = args()
        if not tui_mode:
            assert file_path is not None
            assert algorithm is not None
            hash = run_calculate(file_path, algorithm, compare_hash)
            print(f"{algorithm} value for {get_file_name(file_path)}: {hash}")
            sys.exit(0)

    if tui_mode:
        algorithm = tui_select_algorithm()
        file_path = tui_select_file(algorithm)
        compare_hash = tui_input_hash(algorithm)
    else:
        algorithm = select_algorithm()
        file_path = select_file(algorithm)
        compare_hash = input_hash(algorithm)
    
    print(f"{algorithm} value for {get_file_name(file_path)}: {run_calculate(file_path, algorithm, compare_hash)}") 
    input("Press any key to continue...")
    sys.exit(0)

if __name__ == "__main__":
    main()