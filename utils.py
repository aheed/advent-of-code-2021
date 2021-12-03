import sys

def get_in_file():
    if len(sys.argv) <= 1:
        print("opening stdin")
        inputfile = sys.stdin
    else:
        print("opening input file {}".format(sys.argv[1]))
        inputfile = open(sys.argv[1], "r")
    return inputfile

def get_ints_from_in_file_lines():
    infile = get_in_file()
    ints = [int(line) for line in infile]
    infile.close()
    return ints