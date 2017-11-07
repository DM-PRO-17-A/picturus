import numpy as np
# from numba import double
from numba.decorators import jit
from time import time

# @jit(arg_types=[double[:,:], double[:,:]]) deprecated
@jit(nopython=True)
def pairwise_numba(X, D):
    M = X.shape[0]
    N = X.shape[1]
    for i in range(M):
        for j in range(M):
            d = 0.0
            for k in range(N):
                tmp = X[i, k] - X[j, k]
                d += tmp * tmp
            D[i, j] = np.sqrt(d)
X = np.random.random((1000, 3))
D = np.empty((1000, 1000))
for i in range(100):
	start = time()
        pairwise_numba(X, D)
        print time() - start
