from numpy.random import random
from ecvq import ECVQ

if __name__ == '__main__':
    data = []
    data_num = 2000
    data_dim = 9
    data_range = 30

    for i in xrange(data_num):
        data.append([random()*data_range for i in xrange(data_dim)])

    centroid, centroid_member, centroid_prob = ECVQ(data, 64, 2)
    print centroid_prob
