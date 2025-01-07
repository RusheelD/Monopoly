import sys

def find_no_sweep():
    log_folder = sys.argv[1]
    log_file = log_folder + "/_overview.txt"
    with open(log_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "no sweep" in line and "win" in line:
                print(line,end='')
    print()

if __name__ == "__main__":
    find_no_sweep()