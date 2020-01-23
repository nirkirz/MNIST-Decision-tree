import math
import Condition
import copy

class Image:

    def __init__(self,img):
        self.original_image = img
        self.bounds = None

    def SharpImage(self, img):
        new_img = copy.deepcopy(img)
        for i in range(1, 785):
            if new_img[i] > 64:
                new_img[i] = 255
            else:
                new_img[i] = 0
        return new_img


    def CreateBounderiesImage(self, sharp_img):
        grad = [0]
        for row in range(0, 28):
            for col in range(0, 28):
                grad.append(0)
        for i in range(1, 27):
            for j in range(1, 27):
                left = sharp_img[i * 28 + j] - sharp_img[i * 28 + j - 1]
                right = sharp_img[i * 28 + j] - sharp_img[i * 28 + j + 1]
                up = sharp_img[i * 28 + j] - sharp_img[(i + 1) * 28 + j]
                down = sharp_img[i * 28 + j] - sharp_img[(i - 1) * 28 + j]
                grad[i * 28 + j] = max([left, right, up, down])
        return grad