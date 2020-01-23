import copy
import learningAlgorithm
import numpy as np

class condition:

    def __init__(self, cond_details, cond_type):
        self.cond_details = cond_details
        self.cond_type = cond_type

    def CheckCondition(self, img, bound_pics):
        # ---- Type 1 : Version1 Condition
        # check if each cell is more than more_than ---- #
        if self.cond_type == 1:
            img_index = self.cond_details[0]
            more_than = self.cond_details[1]
            return img[img_index] > more_than
        # ---- Type 2 : Squares
        # check if all cell in each square is more than more_than ---- #
        elif self.cond_type == 2:
            top_left_index = self.cond_details[0]
            size = self.cond_details[1]
            more_than = self.cond_details[2]
            num_to_count = self.cond_details[3]
            counter = 0
            for i in range(size):
                for j in range(size):
                    if img[top_left_index + i*28 + j] > more_than:
                        counter += 1
            return counter >= num_to_count
        # ---- Type 3 : if min/max in row/col i is in col/row j ---- #
        elif self.cond_type == 3:
            min_or_max = self.cond_details[0]
            row_or_col = self.cond_details[1]
            row = self.cond_details[2]
            col = self.cond_details[3]
            # ---- test value saves the value we need to compare at the end of the function
            if row_or_col == "row":
                test_value = col
            else:
                test_value = row
            if row_or_col == "row":
                this_square_value = 0
                for i in range(4):
                    for j in range(4):
                        this_square_value += img[(row+i)*28 + (col+j)]
                for i in range(0, 28, 4):
                    sum = 0
                    for j in range(4):
                        for k in range(4):
                            sum += img[(row+j)*28 + (i+k)]
                    if sum > this_square_value:
                        return False
                return True
            else:
                this_square_value = 0
                for i in range(4):
                    for j in range(4):
                        this_square_value += img[(row+i)*28 + (col+j)]
                for i in range(0, 28, 4):
                    sum = 0
                    for j in range(4):
                        for k in range(4):
                            sum += img[(i+j)*28 + (col+k)]
                    if sum > this_square_value:
                        return False
                return True
        # --- Type 4 : check if total number of cells in img is more than more_than ---- #
        elif self.cond_type == 4:
            num_of_cells = self.cond_details[0]
            more_than = self.cond_details[1]
            counter = 0
            for i in range(1, 785):
                if img[i] > more_than:
                    counter += 1
            return counter >= num_of_cells
        # --- Type5 : check if there is horizontal/vertical line of length 6 in each quarter on the image
        # --- The check is on the bounderies of each digit
        elif self.cond_type == 5:
            # sharpImg = SharpImage(img)
            # bounds = CreateBounderiesImage(sharpImg)
            bound_pics = bound_pics[1]
            bounds = bound_pics[img[785]]
            if self.cond_details[0] == "horizontal":
                start_of_row = self.cond_details[1]
                for i in range(start_of_row, start_of_row+28*7, 28):
                    counter = 0
                    for j in range(0, 28):
                        if bounds[i+j] == 255:
                            counter += 1
                            if counter == self.cond_details[2]:
                                return True
                        else:
                            counter = 0
                return False
            else:
                start_of_col = self.cond_details[1]
                for i in range(start_of_col, start_of_col+7):
                    counter = 0
                    for j in range(0, 28*28, 28):
                        if bounds[i+j] == 255:
                            counter += 1
                            if counter == self.cond_details[2]:
                                return True
                        else:
                            counter = 0
                return False
        elif self.cond_type == 6:
            sharp_pics = bound_pics[0]
            loc = self.cond_details[0]
            ind = False
            if sharp_pics[img[785]][loc] == 0:
                ind = True
            elif sharp_pics[img[785]][loc-1] == 0:
                loc = loc - 1
                ind = True
            elif sharp_pics[img[785]][loc+1] == 0:
                loc = loc + 1
                ind = True
            elif sharp_pics[img[785]][loc-28] == 0:
                loc = loc - 28
                ind = True
            elif sharp_pics[img[785]][loc+28] == 0:
                loc = loc + 28
                ind = True
            elif sharp_pics[img[785]][loc-27] == 0:
                loc = loc - 27
                ind = True
            elif sharp_pics[img[785]][loc+27] == 0:
                loc = loc + 27
                ind = True
            elif sharp_pics[img[785]][loc-29] == 0:
                loc = loc - 29
                ind = True
            elif sharp_pics[img[785]][loc+29] == 0:
                loc = loc + 29
                ind = True
            if ind == False:
                return False
            else:
                return is_hole(loc, sharp_pics[img[785]])
        # Check diagonals
        elif self.cond_type == 7:
            sum = 0
            if self.cond_details[1] == 0:
                for i in range(3):
                    for j in range(3):
                        if img[28*i + j] > 128:
                            sum += 1
                for i in range(1, 25):
                    if img[28*(i+1) + i + 3] > 128:
                        sum += 1
                    if img[28*(i+2) + i + 3] > 128:
                        sum += 1
                    if img[28*(i+3) + i + 3] > 128:
                        sum += 1
                    if img[28*(i+3) + i + 2] > 128:
                        sum += 1
                    if img[28*(i+3) + i + 1] > 128:
                        sum += 1
            else:
                for i in range(3):
                    for j in range(27, 24, -1):
                        if img[28*i + j] > 128:
                            sum += 1
                for i in range(1, 25):
                    if img[28*(i+1) + (27 - i) - 3] > 128:
                        sum += 1
                    if img[28*(i+2) + (27 - i) - 3] > 128:
                        sum += 1
                    if img[28*(i+3) + (27 - i) - 3] > 128:
                        sum += 1
                    if img[28*(i+3) + (27 - i) - 2] > 128:
                        sum += 1
                    if img[28*(i+3) + (27 - i) - 1] > 128:
                        sum += 1
            if sum >= self.cond_details[0]:
                return True
            else:
                return False


# check if each cell is more than more_than ---- #
def BuildVersion1ConditionArray():
    conds = []
    for i in range(1, 785):
        cond = condition([i, 128], 1)
        conds.append(cond)
    return conds

# check if 3 or 5 cells in each square is more than more_than ---- #
def BuildType2ConditionArray():
    conds = []
    for i in range(3, 4):
        for row in range(0, 28-i+1):
            for col in range(0,28-i+1):
                cond = condition([row*28+col, i, 128, 3], 2)
                conds.append(cond)
                cond = condition([row*28+col, i, 128, 5], 2)
                conds.append(cond)
    return conds

# ---- Type 3 : if min/max in row/col i is in col/row j ---- #
def BuildType3ConditionArrayOLDVERSION():
    conds = []
    min_max = ["min", "max"]
    row_col = ["row", "col"]
    for m in min_max:
        for n in row_col:
            for i in range(28):
                for j in range(28):
                    cond = condition([m, n, i, j], 3)
                    conds.append(cond)
    return conds

# ---- Type 3 : if min/max in row/col i is in col/row j ---- #
def BuildType3ConditionArray():
    conds = []
    min_max = ["min", "max"]
    row_col = ["row", "col"]
    for m in min_max:
        for n in row_col:
            for i in range(0, 28, 4):
                for j in range(0, 28, 4):
                    cond = condition([m, n, i, j], 3)
                    conds.append(cond)
    return conds


# --- Type 4 : check if total number of cells in img is more than more_than ---- #
def BuildType4ConditionArray():
    conds = []
    for i in range (50, 785, 50):
        cond1 = condition([i, 128], 4)
        cond2 = condition([i, 64], 4)
        cond3 = condition([i, 192], 4)
        conds.append(cond1)
        conds.append(cond2)
        conds.append(cond3)
    return conds


# --- Type5 : check if there is horizontal/vertical line of length 6 in each quarter on the image
# --- The check is on the bounderies of each digit
def BuildType5ConditionArray():
    conds = []
    for i in range(1,5):
        for j in range (5,8):
            cond1 = condition(["horizontal", (i-1)*28*7 + 1, j], 5)
            cond2 = condition(["vertical", (i-1)*7 + 1, j], 5)
            conds.append(cond1)
            conds.append(cond2)
    return conds


def BuildType6ConditionArray():
    conds = []
    i = 3
    for row in range(0, 28-i+1):
        for col in range(0,28-i+1):
            cond = condition([(row+1)*28+col+1], 6)
            conds.append(cond)
    return conds


def BuildType7ConditionArray():
    conds = []
    for i in range (28):
        cond = condition([25, 0, 0], 7)
        conds.append(cond)
        cond = condition([50, 0, 0], 7)
        conds.append(cond)
        cond = condition([75, 0, 0], 7)
        conds.append(cond)
        cond = condition([100, 0, 0], 7)
        conds.append(cond)
        cond = condition([25, 27, 27], 7)
        conds.append(cond)
        cond = condition([50, 27, 27], 7)
        conds.append(cond)
        cond = condition([75, 27, 27], 7)
        conds.append(cond)
        cond = condition([100, 27, 27], 7)
        conds.append(cond)
    return conds


def SharpImage(img):
    new_img = copy.deepcopy(img)
    for i in range(1, 785):
        if new_img[i] > 64:
            new_img[i] = 255
        else:
            new_img[i] = 0
    return new_img


def CreateBounderiesImage(sharp_img):
    grad = [0]
    for row in range (0, 28):
        for col in range(0, 28):
            grad.append(0)
    for i in range(1,27):
        for j in range(1, 27):
            left = sharp_img[i*28 + j] - sharp_img[i*28 + j - 1]
            right = sharp_img[i*28 + j] - sharp_img[i*28 + j + 1]
            up = sharp_img[i*28 + j] - sharp_img[(i+1)*28 + j]
            down = sharp_img[i*28 + j] - sharp_img[(i-1)*28 + j]
            grad[i*28 + j] = max([left, right, up, down])
    return grad

def is_hole(loc, img):
    img = img[1:785]
    img = np.reshape(img, (-1,28))
    loc_row = int(loc/28)
    loc_col = loc%28
    total_flag = True

    col = loc_col
    row = loc_row
    while(row >= 0):
        if img[row,col] == 255:
            break
        else:
            row = row-1
    if row < 0:
        total_flag = False

    col = loc_col
    row = loc_row
    while(row <= 27 and total_flag):
        if img[row,col] == 255:
            break
        else:
            row = row+1
    if row == 28:
        total_flag = False

    col = loc_col
    row = loc_row
    while(col <= 27 and total_flag):
        if img[row,col] == 255:
            break
        else:
            col = col+1
    if col == 28:
        total_flag = False

    col = loc_col
    row = loc_row
    while(col >= 0 and total_flag):
        if img[row,col] == 255:
            break
        else:
            col = col-1
    if col < 0:
        total_flag = False

    col = loc_col
    row = loc_row
    while(col >= 0 and row >= 0 and total_flag):
        if img[row,col] == 255:
            break
        else:
            col = col-1
            row = row-1
    if col < 0 or row < 0:
        total_flag = False

    col = loc_col
    row = loc_row
    while(col <= 27 and row >= 0 and total_flag):
        if img[row,col] == 255:
            break
        else:
            col = col+1
            row = row-1
    if col == 28 or row < 0:
        total_flag = False

    col = loc_col
    row = loc_row
    while(col <= 27 and row <= 27 and total_flag):
        if img[row,col] == 255:
            break
        else:
            col = col+1
            row = row + 1
    if col == 28 or row == 28:
        total_flag = False

    col = loc_col
    row = loc_row
    while(col >= 0 and row <= 27 and total_flag):
        if img[row,col] == 255:
            break
        else:
            col = col-1
            row = row + 1
    if col < 0 or row == 28:
        total_flag = False

    return total_flag