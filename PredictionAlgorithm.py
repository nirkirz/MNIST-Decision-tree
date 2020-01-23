import ReadCsvFiles
import BinTree
import Condition
import random
import math
import pickle
import sys

# Function for self use. DELETE!!!
def print_conds(tree):
    if tree is None:
        return
    if not tree.cond == None:
        print(tree.cond.cond_type)
        print(tree.cond.cond_details)
    print_conds(tree.left)
    print_conds(tree.right)

def main():
    '''
    tree_file = sys.argv[1]
    test_file = sys.argv[2]
    '''
    tree_file = "out"
    test_file = "mnist_test.csv"

    file = open(tree_file, 'rb')
    tree = pickle.load(file)

    print_conds(tree) #DELETE!!!

    tests_img = ReadCsvFiles.FileToSet(test_file)

    bound_pics = []
    sharp_pics = []
    pic_id = 0
    for pic in tests_img:
        print(pic_id)
        pic.append(pic_id)
        sharped = Condition.SharpImage(pic)
        sharp_pics.append(sharped)
        bound_pics.append(Condition.CreateBounderiesImage(sharped))
        pic_id += 1

    good = 0
    for img in tests_img:
        to_print = BinTree.getLabelByTree(tree, img, [sharp_pics,bound_pics])
        print(to_print)
        if img[0] == to_print:
            good += 1

    print(good/len(tests_img)*100) #DELETE! ONLY FOR PRIVATE USE! NOT FOR SUBMISSION


if __name__ == "__main__":
    main()
