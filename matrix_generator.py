import numpy as np
import cv2
import matplotlib.pyplot as plt


matr=np.matrix(([[0,0, 1004], 0, 0, 0, 0,0, 0],
               [0, 0, [101,  28, 130],[202,  28, 127],[303,  28, 124],[404,  29, 120],[505,  29, 117]]),
               dtype=np.ndarray)


print matr.shape
print matr

matr_shape = matr.shape

spa_X_array = np.array([])
spa_Y_array = np.array([])
val_X_array = np.zeros((matr_shape[0], matr_shape[1]), dtype=np.uint32)
val_Y_array = np.zeros((matr_shape[0], matr_shape[1]), dtype=np.uint32)
n_row_matr = matr_shape[0]
n_col_matr = matr_shape[1]
matr_row_count = 0
while matr_row_count < n_row_matr:
    matr_col_count = 0
    while matr_col_count < n_col_matr:
        matr_value = matr[matr_row_count, matr_col_count]
        if matr_value!=0:
            val_X_array[matr_row_count, matr_col_count] = matr_value[0]
            val_Y_array[matr_row_count, matr_col_count] = matr_value[1]
        else:
            val_X_array[matr_row_count, matr_col_count] = 0
            val_Y_array[matr_row_count, matr_col_count] = 0
        matr_col_count = matr_col_count + 1
    matr_row_count = matr_row_count + 1

print val_X_array
print val_Y_array
