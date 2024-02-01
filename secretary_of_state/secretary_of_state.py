import sys

def usage():
    print("secretary-of-state:")
    print("\tconverts csv state machines to mermaid diagrams")
    print("usage:")
    print("\tsecretary [file]")
    print("")
    print("\t[file]: path to a csv file")

def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    print("FATAL: secretary is not yet implemented ;-;")
    print("please come back later")