class condition:

    def __init__(self, img_index, more_than):
        self.img_index = img_index
        self.more_than = more_than

    def CheckCondition(self,img):
        return img[self.img_index] > self.more_than


def BuildVersion1ConditionArray():
    conds = []
    for i in range(1,749):
        cond = condition(i, 128)
        conds.append(cond)
    return conds
