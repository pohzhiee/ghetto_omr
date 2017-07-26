import numpy as np
import cv2
from edcamcam_testfile_shape import shapedetector
import matplotlib.pyplot as plt


matr=np.matrix(([[0,0, 1004], 0, 0, 0, 0,0, 0],
               [0, 0, [101,  28, 130],[202,  28, 127],[303,  28, 124],[404,  29, 120], [505,  29, 117]]),
               dtype=np.ndarray)


print matr.shape
print matr

matr_shape = matr.shape

spa_X_array = np.array([])
spa_Y_array = np.array([])
val_X_array = np.zeros((matr_shape[0], matr_shape[1]), dtype=np.uint8)
val_Y_array = np.zeros((matr_shape[0], matr_shape[1]), dtype=np.uint8)

counter_g1 = 0
while counter_g1 < matr_shape[1]:
    counter_g2 = 0
    while counter_g2 < matr_shape[0]:
        matr_value = matr[counter_g2, counter_g1]
        if matr_value!=0:
            val_X_array[counter_g2, counter_g1] = matr_value[1]
            val_Y_array[counter_g2, counter_g1] = matr_value[0]
        else:
            val_X_array[counter_g2, counter_g1] = 0
            val_Y_array[counter_g2, counter_g1] = 0
        counter_g2 = counter_g2 + 1
    counter_g1 = counter_g1 + 1

print val_X_array
print val_Y_array
