import ReadCsvFiles
import BinTree
import Condition
import random
import math
import pickle
import sys

def main():
    '''
    tree_file = sys.argv[1]
    test_file = sys.argv[2]
    '''
    tree_file = "out"
    test_file = "mnist_test.csv"

    file = open(tree_file, 'rb')
    tree = pickle.load(file)

    tests = ReadCsvFiles.FileToSet(test_file)

    good = 0
    for test in tests:
        to_print = BinTree.getLabelByTree(tree, test)
        print(to_print)
        if test[0] == to_print:
            good += 1

    print(good/len(tests)*100)


if __name__ == "__main__":
    main()
