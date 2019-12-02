import csv


def FileToSet(file):
    with open(file, 'r') as mnist_file:
        reader = csv.reader(mnist_file, delimiter=',')
        pictures = []

        for row in reader:
            pictures.append(row)

        for i in range(len(pictures)):
            for j in range(len(pictures[i])):
                pictures[i][j] = int(pictures[i][j])

        return pictures

