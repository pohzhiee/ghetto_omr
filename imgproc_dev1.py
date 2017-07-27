import numpy as np
import cv2
import matplotlib.pyplot as plt
import imgproc_funcfile as imgfunc

#Part 1: Image Loading
#-------------------------------------------------------------------

#load image
img = cv2.imread('img_data/omstest2.jpg',cv2.IMREAD_GRAYSCALE)
img2= cv2.imread('img_data/omstest2.jpg')
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
# 4)Pick top n number str and column
def OptMatFunc(matrix_grid,n_row,n_col):
    bin_matr = MatBinFunc(matrix_grid)
    row_sum=np.sum(bin_matr,axis=1)
    col_sum = np.sum(bin_matr, axis=0)

    matr_shape=bin_matr.shape
    str_matr=np.zeros((matr_shape[0],matr_shape[1]),dtype=np.uint16)

    m=0
    while m<matr_shape[0]:
        n=0
        while n<matr_shape[1]:
            str_matr[m, n]=(row_sum[m]+col_sum[n]-2)*bin_matr[m,n]
            n=n+1
        m=m+1

    row_sum_str = np.sum(str_matr, axis=1)
    col_sum_str = np.sum(str_matr, axis=0)


    row_sum_str_sort=np.sort(row_sum_str,0,'mergesort')
    col_sum_str_sort = np.sort(col_sum_str,0, 'mergesort')

    min_row=row_sum_str_sort[len(row_sum_str_sort)-n_row]
    min_col=col_sum_str_sort[len(col_sum_str_sort)-n_col]

    x=0
    compress_criteria_row = np.array([])
    while x<len(row_sum_str):
        if row_sum_str[x]<min_row:
            compress_criteria_row = np.append(compress_criteria_row, 0)
        else:
            compress_criteria_row=np.append(compress_criteria_row,1)
        x=x+1
    y = 0
    compress_criteria_col = np.array([])
    while y < len(col_sum_str):
        if col_sum_str[y] < min_col:
            compress_criteria_col = np.append(compress_criteria_col, 0)
        else:
            compress_criteria_col=np.append(compress_criteria_col,1)
        y=y+1

    if n_row!=np.sum(compress_criteria_row):
        print "gg row"
    if n_col != np.sum(compress_criteria_col):
        print "gg col"


    opt_matr_init =np.compress(compress_criteria_row,matrix_grid,axis=0)
    opt_matr = np.compress(compress_criteria_col, opt_matr_init, axis=1)

    return opt_matr


print "----------------------------------------"

new_matrix_grid=OptMatFunc(matrix_grid,10,8)
new_matrix_grid=new_matrix_grid.reshape(new_matrix_grid.shape[0]*new_matrix_grid.shape[1])

newer_matrix_grid=np.zeros((new_matrix_grid.shape[0],3),dtype=np.uint32)
k=0
while k<new_matrix_grid.shape[0]:
    g=new_matrix_grid[k]
    newer_matrix_grid[k,0]=g[0]
    newer_matrix_grid[k,1]=g[1]
    newer_matrix_grid[k,2]=g[2]
    k=k+1

#checkpoint
#print centpt_array
# print '-----------'
#print len(centpt_array)





#initialise plot
plt.subplot(111),plt.imshow(img3)
plt.title('dilate1 Image'), plt.xticks([]), plt.yticks([])
for k in newer_matrix_grid:
    plt.plot(k[0],k[1],'ro')


plt.show()

cv2.waitKey(0)



