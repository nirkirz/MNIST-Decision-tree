import ReadCsvFiles
import BinTree
import Condition
import random
import math
import pickle
import sys
import time
import threading
import json
import multiprocessing as mp

def BuildDecisionTree(t,train_set, conds, bound_pics, tree, leaves, id_leaf, last_t):
    with open('bound.json', 'w') as f:
        json.dump(bound_pics, f)
    print("T: " + str(t))
    begin = time.time()
    for i in range(last_t, t):
        print("Working stage : " + str(i))
        # ---- Variables to save optimal X and L ---- #
        max_value = 0
        max_L = None
        max_X = None
        max_la_examples = None
        max_lb_examples = None
        # ---- End Initial Variables ---- #

        t_init = [False, False]

        for L in leaves:
            # Find Optimal X for each leaf
            local_max_value = 0
            local_max_X = None
            local_max_la_examples = None
            local_max_lb_examples = None
            jobs = []
            if len(L.IG_details) == 0:  # If leaf did not calculated before
                if not t_init[0]:
                    t_init[0] = True
                    T1 = mp.Process(target=NewLeafCalculation,
                                          args=(conds, L, local_max_value, local_max_X, local_max_la_examples,
                                                local_max_lb_examples))
                    jobs.append(T1)
                    T1.start()
                    print("T1 started... ")
                else:
                    t_init[1] = True
                    T2 = mp.Process(target=NewLeafCalculation,
                                          args=(conds, L, local_max_value, local_max_X, local_max_la_examples,
                                                local_max_lb_examples))
                    jobs.append(T2)
                    T2.start()
                    print("T2 started... ")

                # NewLeafCalculation(conds, bound_pics, L, local_max_value, local_max_X, local_max_la_examples,
                #                    local_max_lb_examples)
                # for X in conds:
                #     la = []
                #     lb = []
                #     for ex in L.examples:
                #         if X.CheckCondition(ex, bound_pics):
                #             la.append(ex)
                #         else:
                #             lb.append(ex)
                #     h_la = BinTree.H(la)
                #     h_lb = BinTree.H(lb)
                #     n = len(L.examples)
                #     h_x = len(la)/n * h_la + len(lb)/n * h_lb
                #     h_l = BinTree.H(L.examples)
                #     IG_X_L = h_l - h_x
                #     if(local_max_value < IG_X_L*n):
                #         local_max_value = IG_X_L*n
                #         local_max_X = X
                #         local_max_la_examples = la
                #         local_max_lb_examples = lb
                # L.IG_details = [local_max_value, local_max_X, local_max_la_examples, local_max_lb_examples]
        for job in jobs:
            job.join()
        for L in leaves:
            if max_value < L.IG_details[0]:
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

        total_calc_time = time.time() - begin
        print("Total time for tree calculation: " + str(total_calc_time))
        print("")
    return [tree, leaves, id_leaf]


def NewLeafCalculation(conds, L, local_max_value, local_max_X, local_max_la_examples, local_max_lb_examples):
    with open ('bounds.json', 'r') as f:
        bound_pics = json.load(f)
    for X in conds:
        la = []
        lb = []
        for ex in L.examples:
            if X.CheckCondition(ex, bound_pics):
                la.append(ex)
            else:
                lb.append(ex)
        h_la = BinTree.H(la)
        h_lb = BinTree.H(lb)
        n = len(L.examples)
        h_x = len(la) / n * h_la + len(lb) / n * h_lb
        h_l = BinTree.H(L.examples)
        IG_X_L = h_l - h_x
        if (local_max_value < IG_X_L * n):
            local_max_value = IG_X_L * n
            local_max_X = X
            local_max_la_examples = la
            local_max_lb_examples = lb
    L.IG_details = [local_max_value, local_max_X, local_max_la_examples, local_max_lb_examples]

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

    start_time = time.time()
    bound_pics = []

    version = 2
    p = 20
    l = 5
    train_set_file_name = "mnist_train.csv"
    output_tree_file_name = "out"

    pictures = ReadCsvFiles.FileToSet(train_set_file_name)

    cond_nums = [1, 2, 3, 5, 6]
    # # NOT FOR SUBMISSION
    # random.shuffle(pictures)
    # pictures = pictures[:5000]

    # ---- in case condition 5 is been used, we will build the bounded pics and set in global array ----
    if (5 in cond_nums or 6 in cond_nums):
        print("Creating bounderies and sharped images...")
        print("")
        sharp_pics = []
        bound_pics1 = []
        pic_id = 0
        for pic in pictures:
            print(pic_id)
            pic.append(pic_id)
            sharped = Condition.SharpImage(pic)
            sharp_pics.append(sharped)
            bound_pics1.append(Condition.CreateBounderiesImage(sharped))
            pic_id += 1
        bound_pics = [sharp_pics, bound_pics1]

    random.shuffle(pictures)
    valid_set_size = int(p/100*len(pictures))
    valid_set = pictures[0:valid_set_size]
    train_set = pictures[valid_set_size:]
    conds = []

    if(version == 1):
        conds = Condition.BuildVersion1ConditionArray()
    else:
        conds1 = Condition.BuildVersion1ConditionArray()
        conds2 = Condition.BuildType2ConditionArray()
        conds3 = Condition.BuildType3ConditionArray()
        conds5 = Condition.BuildType5ConditionArray()
        conds6 = Condition.BuildType6ConditionArray()
        conds = conds1 + conds2 + conds3 + conds5 + conds6
        # conds = conds1 + conds2 + conds3



    t_trees = []
    id_leaf = 1
    # ---- Build first leaf ----
    max_digit = BinTree.common_label(train_set)
    tree = BinTree.BinTree(None, max_digit,id_leaf)
    id_leaf += 1
    tree.examples = train_set
    # ---- End build first leaf ----

    last_t = 0
    leaves = [tree]
    max_l = -1
    max_value = 0
    for i in range(l+1):
        res_build = BuildDecisionTree(int(math.pow(2,i)), train_set, conds, bound_pics, tree, leaves, id_leaf, last_t)
        t_trees.append(res_build[0])
        tree = res_build[0]
        leaves = res_build[1]
        id_leaf = res_build[2]
        last_t = int(math.pow(2,i))

        succeeded = 0
        for img in valid_set:
            predicted_label = BinTree.getLabelByTree(tree, img, bound_pics)
            if(predicted_label == img[0]):
                succeeded += 1
        if (max_value < succeeded):
            max_value = succeeded
            max_l = i


    # Find tree with optimal L value
    # max_l = -1
    # max_value = 0
    # for i in range(len(t_trees)):
    #     succeeded = 0
    #     for img in valid_set:
    #         predicted_label = BinTree.getLabelByTree(t_trees[i],img, bound_pics)
    #         if(predicted_label == img[0]):
    #             succeeded += 1
    #     if (max_value < succeeded):
    #         max_value = succeeded
    #         max_l = i

    # ---- Build Final Tree ----
    id_leaf = 1
    # ---- Build first leaf ----
    max_digit = BinTree.common_label(train_set)
    tree = BinTree.BinTree(None, max_digit, id_leaf)
    id_leaf += 1
    tree.examples = train_set
    # ---- End build first leaf ----

    last_t = 0
    leaves = [tree]
    final_t = int(math.pow(2,max_l))
    res_final = BuildDecisionTree(final_t,pictures,conds, bound_pics, tree, leaves, id_leaf, last_t)
    final_tree = res_final[0]
    # ---- Finish Build Final Tree ----

    filehandler = open(output_tree_file_name,'wb')
    pickle.dump(final_tree, filehandler)

    print("num: " + str(len(train_set)))
    errors = 0
    for img in pictures:
        predicted_label = BinTree.getLabelByTree(final_tree, img, bound_pics)
        if (predicted_label != img[0]):
            errors += 1

    print("error: " + str(errors))
    print("size: " + str(final_t))

    print("TIME: " + str(time.time() - start_time)) #NOT FOR SUBMISSION!!!

if __name__ == "__main__":
    main()
