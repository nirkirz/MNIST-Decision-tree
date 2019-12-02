import math

class BinTree:

    def __init__(self,cond,label,id):
        self.right = None
        self.left = None
        self.cond = cond
        self.label = label
        self.examples = []
        self.id = id
        self.IG_details=[]

    def isLeaf(self):
        return self.right is None and self.left is None

    def __eq__(self, other):
        return self.id == other.id


def H(leaf_examples):
    Ni = []
    for i in range(10):
        Ni.append(0)

    for ex in leaf_examples:
        Ni[ex[0]] += 1

    h_value = 0
    n = len(leaf_examples)
    for ni in Ni:
        if n == 0 or ni == 0:
            h_value += 0
        else:
            h_value += (ni/n)*math.log(n/ni, 10)

    return h_value


def common_label(train_set):
    digit_count = []
    for i in range(10):
        digit_count.append(0)

    for pic in train_set:
        digit_count[pic[0]] += 1

    max_digit = -1
    max_i = -1
    for i in range(len(digit_count)):
        dig = digit_count[i]
        if dig > max_digit:
            max_digit = dig
            max_i = i

    return max_i

def getLabelByTree(tree, img):
    while tree.isLeaf() == False:
        if tree.cond.CheckCondition(img):
            tree = tree.right
        else:
            tree = tree.left
    return tree.label
