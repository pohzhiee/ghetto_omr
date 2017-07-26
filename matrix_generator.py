import numpy as np
import cv2
from edcamcam_testfile_shape import shapedetector
import matplotlib.pyplot as plt


#matr_generator

p=1
q=1

while p<4:
    while q<4:
        matr = np.zeros((p, q), dtype=np.uint8)
        print matr
        k=0
        while k < 2**(p+q-1)-1:
            g=0
            while g < p*q:
                i=0
                j=0
                while i < p:

                    while j < q:
                        if matr[i, j] == 1:
                            matr[i, j] == 0
                        elif matr[i, j] == 0:
                            matr[i, j] = 1
                            print matr
                            break
                        j = j + 1
                    else:
                        continue

                    break
                    i = i + 1
                g=g+1
            k=k+1
        q=q+1
    p=p+1

