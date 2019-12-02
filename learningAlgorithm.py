import ReadCsvFiles
import BinTree
import Condition
import random
import math
import pickle
import sys


def BuildDecisionTree(t,train_set, conds):
    id_leaf = 1
    # ---- Build first leaf ----
    max_digit = BinTree.common_label(train_set)
    tree = BinTree.BinTree(None, max_digit,id_leaf)
    id_leaf += 1
    tree.examples = train_set
    # ---- End build first leaf ----

    leaves = [tree]
    for i in range(t):
        max_value = 0
        max_L = None
        max_X = None
        max_la_examples = None
        max_lb_examples = None
        for L in leaves:
            local_max_value = 0
            local_max_X = None
            local_max_la_examples = None
            local_max_lb_examples = None
            if (len(L.IG_details) == 0):
                for X in conds:
                    la = []
                    lb = []
                    for ex in L.examples:
                        if X.CheckCondition(ex):
                            la.append(ex)
                        else:
                            lb.append(ex)
                    h_la = BinTree.H(la)
                    h_lb = BinTree.H(lb)
                    n = len(L.examples)
                    h_x = len(la)/n * h_la + len(lb)/n * h_lb
                    h_l = BinTree.H(L.examples)
                    IG_X_L = h_l - h_x
                    if(local_max_value < IG_X_L*n):
                        local_max_value = IG_X_L*n
                        local_max_X = X
                        local_max_la_examples = la
                        local_max_lb_examples = lb
                L.IG_details = [local_max_value, local_max_X, local_max_la_examples, local_max_lb_examples]
            if (max_value < L.IG_details[0]):
                max_value = L.IG_details[0]
                max_L = L
                max_X = L.IG_details[1]
                max_la_examples = L.IG_details[2]
                max_lb_examples = L.IG_details[3]

        # ---- Build Chosen leaf ----
        leaf_la = BinTree.BinTree(None,BinTree.common_label(max_la_examples),id_leaf)
        id_leaf += 1
        leaf_la.examples = max_la_examples
        leaf_lb = BinTree.BinTree(None,BinTree.common_label(max_lb_examples), id_leaf)
        id_leaf += 1
        leaf_lb.examples = max_lb_examples
        max_L.left = leaf_lb
        max_L.right = leaf_la
        max_L.label = None
        max_L.cond = max_X
        leaves.remove(max_L)
        leaves.append(leaf_la)
        leaves.append(leaf_lb)
        # ---- End Build Chosen Leaf ----

    return tree


def main():
    '''
    version = sys.argv[1]
    p = sys.argv[2]
    l = sys.argv[3]
    train_set_file_name = sys.argv[4]
    output_tree_file_name = sys.argv[5]
    '''

    '''
    print("Enter Version")
    version = int(input())
    print("Enter p value")
    p = int(input())
    l = int(input("Enter l value"))
    train_set_file_name = input("Enter train set file")
    output_tree_file_name = input("Enter output file")
    '''

    version = 1
    p = 20
    l = 4
    train_set_file_name = "mnist_train.csv"
    output_tree_file_name = "out"

    pictures = ReadCsvFiles.FileToSet(train_set_file_name)

    random.shuffle(pictures)
    valid_set_size = int(p/100*len(pictures))
    valid_set = pictures[0:valid_set_size]
    train_set = pictures[valid_set_size:]
    conds = []

    if(version == 1):
        conds = Condition.BuildVersion1ConditionArray()

    t_trees = []
    for i in range(l):
        t_trees.append(BuildDecisionTree(int(math.pow(2,i)), train_set, conds))

    max_l = -1
    max_value = 0
    for i in range(len(t_trees)):
        succeeded = 0
        for img in valid_set:
            predicted_label = BinTree.getLabelByTree(t_trees[i],img)
            if(predicted_label == img[0]):
                succeeded += 1
        if (max_value < succeeded):
            max_value = succeeded
            max_l = i

    final_t = int(math.pow(2,l))
    final_tree = BuildDecisionTree(final_t,pictures,conds)

    filehandler = open(output_tree_file_name,'wb')
    pickle.dump(final_tree, filehandler)

    print("num: " + str(len(train_set)))
    errors = 0
    for img in pictures:
        predicted_label = BinTree.getLabelByTree(final_tree, img)
        if (predicted_label != img[0]):
            errors += 1

    print("error: " + str(errors))
    print("size: " + str(final_t))


if __name__ == "__main__":
    main()
