import numpy as np
import itertools
p=3
q=2
num_bits = p*q
matr = np.empty((p,q),np.uint8)
lst = list(itertools.product([0, 1], repeat=num_bits))
for mat_bin in lst:
    for i in range(p):
        matr[i,:]=mat_bin[i*q:(i+1)*q]
    print matr


