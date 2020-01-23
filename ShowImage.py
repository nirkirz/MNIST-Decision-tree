import numpy as np
import matplotlib.pyplot as plt

def ShowImg(data):
    label = data[0]

    # The rest of columns are pixels
    pixels = data[1:]

    # Make those columns into a array of 8-bits pixels
    # This array will be of 1D with length 784
    # The pixel intensity values are integers from 0 to 255
    pixels = np.array(pixels, dtype='uint8')

    # Reshape the array into 28 x 28 array (2-dimensional array)
    pixels = pixels.reshape((3, 3))

    # Plot
    plt.title('Label is {label}'.format(label=label))
    plt.imshow(pixels, cmap='gray')
    plt.show()


def main():
    ShowImg([0,255,255,255,0,0,0,255,0,255])

if __name__ == "__main__":
    main()