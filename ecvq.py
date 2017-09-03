import numpy as np
from numpy.random import random
from operator import add, div
from math import sqrt, log
import copy

def dist(a, b):
    return (((a - b)**2).sum())**0.5

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

def ECVQ(data, k, l, max_iters=300):
    """ k is the maximum number of clusters, l is the lagrange limitation """

    # Initial variables
    total = len(data)
    alpha = 1e-12
    matrix = np.zeros(k)
    cache = np.zeros((total, k))
    mapping = np.zeros(total).astype(int)
    update_list = np.ones(k).astype(int)

    # Force lookup table enumerate all possible lambda force
    force = [ l * log( (float(i)/total)+alpha ) for i in xrange(total)]

    # Initial the centroid with kmeans++
    centroid = init(data, k)

    for iters in xrange(max_iters):
        diff = 0

        # Assign each data point to its cluster
        centroid_member = [ [] for _ in centroid ]
        next_update = np.zeros_like(update_list).astype(int)

        for i in xrange(total):
            for j in xrange(k):
                if update_list[j]:
                    matrix[j] = dist(data[i], centroid[j])-force[len(centroid_member[j])]
                    cache[i][j] = matrix[j]
                else:
                    matrix[j] = cache[i][j]

            classes = matrix.argmin()
            diff += matrix.min()

            t = mapping[i]
            if t != classes:
                next_update[t] = 1
                next_update[classes] = 1
            mapping[i] = classes
            centroid_member[classes].append(i)

        # Update centroids
        update_id = 0
        updated = np.zeros_like(data[0])
        for c in centroid_member:
            if len(c) and next_update[update_id]:
                for i in xrange(len(c)):
                    updated += data[c[i]]
                updated /= len(c)
                centroid[update_id] = copy.deepcopy(updated)
            update_id += 1
        update_list = copy.deepcopy(next_update)

        count = 0
        for c in centroid_member:
            if len(c) > 0:
                count += 1

        print iters, diff, count

    return centroid, centroid_member, mapping
