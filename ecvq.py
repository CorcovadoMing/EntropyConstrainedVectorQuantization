from numpy.random import random
from operator import add, div
from math import sqrt, log

def dist(a, b):
    result = 0
    for i in xrange(len(a)):
        result += (a[i] - b[i])**2
        # Potential performance trick
        # (a-b)**2 = a**2 + b**2 - (ab+ab), where a**2 and b**2 can be cached!
    return sqrt(result)

def init(data, k):
    """ kmeans++ initialization """
    centroid = [data[int(len(data)*random())]]

    # Cache dist table to prevent duplicate computations
    cache = [-1] * len(data)
    recent_centroid = centroid[0]

    while len(centroid) < k:
        dist_list = []
        for i in xrange(len(data)):
            cadidate = dist(data[i], recent_centroid)
            d = cadidate if cache[i] < 0 else min(cadidate, cache[i])
            cache[i] = d
            dist_list.append(d)
        arrow = sum(dist_list) * random()
        for i in xrange(len(dist_list)):
            arrow -= dist_list[i]
            if arrow <= 0:
                centroid.append(data[i])
                recent_centroid = data[i]
                break
    return centroid

def ECVQ(data, k, l, max_iters=30):
    """ k is the maximum number of clusters, l is the lagrange limitation """

    # Initial variables
    total = len(data)
    update_list = [True] * k
    cache = [[]] * total
    mapping = [0] * total
    force = [ l * log( (i/total)+1e-12 ) for i in xrange(total)]

    # Initial the centroid with kmeans++
    centroid = init(data, k)

    for iters in xrange(max_iters):
        print iters

        # Assign each data point to its cluster
        centroid_member = [ [] for i in centroid ]
        next_update = [False] * k
        for i in xrange(total):

            # (s) Bottle neck
            matrix = [dist(data[i], centroid[j]) - force[len(centroid_member[j])] if update_list[j] else cache[i][j] for j in xrange(k)]
            # (e) Bottle neck

            cache[i] = matrix
            classes = matrix.index(min(matrix))
            t = mapping[i]
            if t != classes:
                next_update[t] = True
                next_update[classes] = True
            mapping[i] = classes
            centroid_member[classes].append(i)

        # Update centroids
        update_id = 0
        for c in centroid_member:
            if len(c) and next_update[update_id]:
                acc = data[c[0]]
                nacc = [float(len(c))] * len(data[0])
                for i in xrange(1, len(c)):
                    acc = map(add, acc, data[c[i]])
                update = map(div, acc, nacc)
                if centroid[update_id] != update:
                    centroid[update_id] = update
            update_id += 1
        update_list = next_update

    return centroid, centroid_member, mapping
