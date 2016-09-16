import csv
import math
import operator
import random
from random import randint

global dataSet


def loadDataset(filename, split):
    trainingSet = []
    testSet = []
    csvfile = open(filename, 'r')
    lines = csv.reader(csvfile)
    dataset = list(lines)
    for x in range(len(dataset) - 1):
        for y in range(4):
            dataset[x][y] = float(dataset[x][y])
    return dataset


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        print instance1[x] , instance2[x]
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance)-1
    for x in range(0,len(trainingSet)-1):
        # print testInstance, trainingSet[x]
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def seperateMinority(dataSet, Minor, classColumnNumber):
    minorSamples = []
    for eachSample in dataSet:
        if (eachSample[classColumnNumber] == Minor):
            minorSamples.append(eachSample)
    return minorSamples


def SMOTE(T, N, minorSamples, numattrs, dataSet, k):
    """
    T = Number of minority class Samples
    Anount of smoted sample required  N%
    k = k mean (clusering value)
    """
    if (N <= 100):
        print "Number of sample to be generated should be more than 100%"
    N = int(N / 100) * T
    Samples = minorSamples
    newindex = 0
    synthetic = []
    for minorSample in Samples:
        # nnarray all nearest neighbour [[2.4, 2.5, 'a'],[2.3, 2.2, 'a'],[2.5, 2.5, 'a']]
        nnarray = getNeighbors(dataSet, minorSample, k)
        print nnarray
    populate(N, minorSample, nnarray, k, numattrs, Samples)


def populate(N, minorSample, nnarray, k, numattrs, Samples):
    synthetic = []
    while (N > 0):
        nn = randint(0, len(Samples) - 1)
        eachUnit = []
        for attr in range(0, numattrs):
            diff = nnarray[nn][attr] - minorSample[attr]
            #             print diff,
            gap = random.uniform(0, 1)
            #             print gap
            eachUnit.append(minorSample[attr] + gap * diff)
        synthetic.append(eachUnit)
        N = N - 1
    print synthetic


numattrs = 4
dataSet = loadDataset('iris.csv', 0.66)
# dataSet
minorSamples = seperateMinority(dataSet, "Iris-virginica", numattrs)
k = 2
SMOTE(3, 200, minorSamples, numattrs - 1, dataSet, k)