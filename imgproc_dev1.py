import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
import imgproc_funcfile as imgfunc

#Part 1: Image Loading
#-------------------------------------------------------------------

#load image
img = cv2.imread('img_data/omstest1.jpg',cv2.IMREAD_GRAYSCALE)
img2= cv2.imread('img_data/omstest1.jpg')
img3=cv2.cvtColor(img.copy(),cv2.COLOR_GRAY2RGB)


outline=imgfunc.outlining(img)
#Part 2: Finding Valid Contours
#-------------------------------------------------------------------
#maximum contour shape matching coefficient


contour_trunc,sum_array,ave_sim_val = imgfunc.contouring(outline)


centpt_array,mean_hor_dist,mean_ver_dist=imgfunc.get_centre(contour_trunc,sum_array,ave_sim_val)



#Part3:Forming Grids
#Assumption: Bubbles are arranged in horinzontal x vertical grid (but not oblique)
#---------------------------------------------------------------------------------------------

#Part3a:Forming grid
#-----------------------------
#Scanning center point x and y and sort
matrix_grid = imgfunc.formgrid(centpt_array,mean_hor_dist,mean_ver_dist)

#Part3b:
#creating function to check spacing are equal for both x and y
def SpaceFunc(matr):
    matr_shape = matr.shape
    spa_X_array = np.array([])
    spa_Y_array = np.array([])
    val_X_matrix = np.zeros((matr_shape[0], matr_shape[1]), dtype=np.ndarray)
    val_Y_matrix = np.zeros((matr_shape[0], matr_shape[1]), dtype=np.ndarray)
    val_X_matrix_counter = np.zeros((matr_shape[0], matr_shape[1]), dtype=np.ndarray)
    val_Y_matrix_counter=np.zeros((matr_shape[0], matr_shape[1]), dtype=np.ndarray)


    counter_g1 = 0
    while counter_g1 < matr_shape[1]:
        counter_g2 = 0
        while counter_g2 < matr_shape[0]:
            matr_value = matr[counter_g2, counter_g1]
            matr_value=np.asarray(matr_value)

            if matr_value.size==3:
                val_X_matrix[counter_g2, counter_g1] = matr_value[0]
                val_Y_matrix[counter_g2, counter_g1] = matr_value[1]
                val_X_matrix_counter[counter_g2, counter_g1] = 1
                val_Y_matrix_counter[counter_g2, counter_g1] = 1
            elif matr_value.size == 0:
                val_X_matrix[counter_g2, counter_g1] = 0
                val_Y_matrix[counter_g2, counter_g1] = 0
                val_X_matrix_counter[counter_g2, counter_g1] = 0
                val_Y_matrix_counter[counter_g2, counter_g1] = 0
            counter_g2 = counter_g2 + 1
        counter_g1 = counter_g1 + 1

    val_X_array_counter = val_X_matrix_counter.sum(axis=0)
    val_Y_array_counter = val_Y_matrix_counter.sum(axis=1)
    val_X_array_acc = val_X_matrix.sum(axis=0)
    val_Y_array_acc=val_Y_matrix.sum(axis=1)
    val_X_array = val_X_array_acc/val_X_array_counter
    val_Y_array = val_Y_array_acc / val_Y_array_counter

    spa_X_array=np.ediff1d(val_X_array)
    spa_Y_array=np.ediff1d(val_Y_array)

#Creating function to convert matrix to binary (those with value to 1, those with 0 to 0)
def MatBinFunc(matr):
    matr_shape = matr.shape
    matr_bin=np.ones((matr_shape[0],matr_shape[1]),dtype=np.uint8)

    counter_g1 = 0
    while counter_g1 < matr_shape[1]:
        counter_g2 = 0
        while counter_g2 < matr_shape[0]:
            matr_value = matr[counter_g2, counter_g1]
            matr_value=np.asarray(matr_value)
            if matr_value.size == 1:
                if matr_value==0:
                    matr_bin[counter_g2, counter_g1]=0

            counter_g2 = counter_g2 + 1
        counter_g1 = counter_g1 + 1
    return matr_bin

#Creating a function to optimise a binary matrix to grid form of 1 x 1
#Methodology:
# 1)Sum rows and columns
# 2)Forming matrix to determine the strength of each cells = (Row.value + Column.value)/2
# 3)Find sum of strength of each column and row
# 4)Defining parameters (
def OptMatFunc(matr,degree):
    row_sum=np.sum(matr,axis=1)
    col_sum = np.sum(matr, axis=0)

    matr_shape=matr.shape
    str_matr=np.zeros((matr_shape[0],matr_shape[1]),dtype=np.uint16)

    m=0
    while m<matr_shape[0]:
        n=0
        while n<matr_shape[1]:
            str_matr[m, n]=(row_sum[m]+col_sum[n]-2)*matr[m,n]
            n=n+1
        m=m+1

    row_sum_str = np.sum(str_matr, axis=1)
    col_sum_str = np.sum(str_matr, axis=0)
    print str_matr
    print row_sum_str
    print col_sum_str

    #calculate half of the strength marker (high and low)
    str_marker_high = matr_shape[0]+matr_shape[1]- math.floor(float(matr_shape[0])/2)-math.floor(float(matr_shape[1])/2)-2
    str_marker_low = matr_shape[0] + matr_shape[1] - math.ceil(float(matr_shape[0]) / 2) - math.ceil(float(matr_shape[1]) / 2) - 2

    # calculate half of the strength multiplier (high and low)
    row_str_multi_high=math.ceil(float(matr_shape[0])/2)
    row_str_multi_low = math.floor(float(matr_shape[0])/2)
    col_str_multi_high=math.ceil(float(matr_shape[1])/2)
    col_str_multi_low = math.floor(float(matr_shape[1]) / 2)

    #for parameter (only odd row or column will make a great difference due to floor and ceiling,
    #even row and column will not show any difference)
    if degree == 1:
        row_str_parameter=str_marker_high*row_str_multi_high
        col_str_parameter = str_marker_high*col_str_multi_high
    elif degree == 2:
        row_str_parameter=str_marker_high*row_str_multi_low
        col_str_parameter = str_marker_high*col_str_multi_low
    elif degree == 3:
        row_str_parameter=str_marker_low*row_str_multi_high
        col_str_parameter = str_marker_low*col_str_multi_high
    elif degree == 4:
        row_str_parameter=str_marker_low*row_str_multi_low
        col_str_parameter = str_marker_low*col_str_multi_low
    else:
        print 'no valid parameter'

    print row_str_parameter
    print col_str_parameter

    p=0
    compress_criteria_row=np.array([])
    while p<matr_shape[0]:
        if row_sum_str[p]<row_str_parameter:
             compress_criteria_row=np.append(compress_criteria_row,0)
        else:
            compress_criteria_row=np.append(compress_criteria_row,1)
        p=p+1

    q=0
    compress_criteria_col= np.array([])
    while q<matr_shape[1]:
        if col_sum_str[q]<col_str_parameter:
             compress_criteria_col=np.append(compress_criteria_col,0)
        else:
            compress_criteria_col=np.append(compress_criteria_col,1)
        q=q+1

    matr=np.compress(compress_criteria_row,matr,axis=0)
    matr= np.compress(compress_criteria_col, matr, axis=1)
    print matr

#Run Matrix Binarisation
bin_matr=MatBinFunc(matrix_grid)
print bin_matr
OptMatFunc(bin_matr,4)
#print x




#checkpoint
#print centpt_array
# print '-----------'
#print valid_counter
#print len(centpt_array)
#print mean_hor_dist
#print mean_ver_dist




#initialise plot
plt.subplot(111),plt.imshow(img3)
plt.title('dilate1 Image'), plt.xticks([]), plt.yticks([])
for k in centpt_array:
    plt.plot(k[0],k[1],'ro')


plt.show()

cv2.waitKey(0)



