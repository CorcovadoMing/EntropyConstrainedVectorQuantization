from numpy.random import random
from ecvq import ECVQ
import numpy as np

if __name__ == '__main__':
    data = []
    data_num = 10000
    data_dim = 9
    cluster = 64

    data = np.random.rand(data_num, data_dim)
    centroid, centroid_member, mapping = ECVQ(data, cluster, 0.015)
