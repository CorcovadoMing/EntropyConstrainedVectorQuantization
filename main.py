from numpy.random import random
from ecvq import ECVQ

if __name__ == '__main__':
    data = []
    data_num = 10000
    data_dim = 9
    data_range = 10
    cluster = 64

    for i in xrange(data_num):
        data.append([random()*data_range for i in xrange(data_dim)])

    centroid, centroid_member, mapping = ECVQ(data, cluster, 2)
