from numpy.random import random
from operator import add, div
import numpy as np
import math

def dist(a, b):
    return np.linalg.norm(np.array(a)-np.array(b))

def init(data, k):
    """ kmeans++ initialization """
    centroid = [data[int(len(data)*random())]]
    while len(centroid) < k:
        dist_list = []
        for i in data:
            dist_list.append(min([dist(i, j) for j in centroid]))
        arrow = sum(dist_list) * random()
        for i in xrange(len(dist_list)):
            arrow -= dist_list[i]
            if arrow <= 0:
                centroid.append(data[i])
                break
    return centroid

def ECVQ(data, k, l):
    """ k is the maximum number of clusters, l is the lagrange limitation """

    # Initial variables
    total = len(data)

    # Initial the centroid with kmeans++
    centroid = init(data, k)
    centroid_prob = [ 0.000000000001 for i in centroid ]

    for times in xrange(10):
        print times
        # Assign each data point to its cluster
        centroid_member = [ [] for i in centroid ]
        for i in xrange(total):
            matrix = [dist(data[i], centroid[j])-(l*math.log(centroid_prob[j])) for j in xrange(k)]
            centroid_member[matrix.index(min(matrix))].append(i)

        # Caculate the prob
        centroid_prob = [ len(i)/float(total) for i in centroid_member ]
        for i in xrange(len(centroid_prob)):
            if centroid_prob[i] == 0:
                # Avoid log(0) error
                centroid_prob[i] = 0.000000000001

        # Update centroids
        update_id = 0
        for c in centroid_member:
            if len(c):
                acc = data[c[0]]
                nacc = [float(len(c)) for i in data[0]]
                for i in xrange(1, len(c)):
                    acc = map(add, acc, data[c[i]])
                centroid[update_id] = map(div, acc, nacc)[:]
            update_id += 1

    return centroid, centroid_member, centroid_prob
