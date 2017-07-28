import numpy as np
import cv2
import matplotlib.pyplot as plt
import imgproc_funcfile as imgfunc

#OMS Info Input
n_col= 8
n_row= 10
path='img_data/omstest2.jpg'

#Settings
show_bubble=1 #0=No, #1=Yes
bubble_colour=(255,0,0)
show_cntpt=1 #0=No, #1=Yes
cntpt_colour=(255,0,0)

#-----------------------------------------------------------------
#Part 1: Image Loading
#load image
img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
img2= cv2.imread(path)
img3=cv2.cvtColor(img.copy(),cv2.COLOR_GRAY2RGB)

#Image Processing (bilateral filter, sharpen, thresh, negative, closed)
outline=imgfunc.outlining(img)

#---------------------------------------------------------------------------------------------
#Part 2: Finding Valid Contours
#maximum contour shape matching coefficient, valid mean Area
#obtain centre point,hor_dist,ver_dist,shape type,shape dimension

contour_trunc,sum_array,ave_sim_val = imgfunc.contouring(outline)
centpt_array,mean_hor_dist,mean_ver_dist,shape_type,shape_dimension=imgfunc.get_centre(contour_trunc,sum_array,ave_sim_val)

#---------------------------------------------------------------------------------------------
#Part3:Forming Grids
#Assumption: Bubbles are arranged in horinzontal x vertical grid (but not oblique)

#form grid as matrix grid
matrix_grid = imgfunc.formgrid(centpt_array,mean_hor_dist,mean_ver_dist)

#form optimised matrix grid
opt_matrix_grid=imgfunc.OptMatFunc(matrix_grid,n_row,n_col)

#---------------------------------------------------------------------------------------------
#converting optimised matrix grid into modified matrix for output
mod_matrix_grid=imgfunc.ModMatrGrid(opt_matrix_grid)

#---------------------------------------------------------------------------------------------
# Adding appropriate shapes and centre points into img3
if show_bubble==1:
    imgoutput=imgfunc.DrawShape(img3,mod_matrix_grid,shape_type,shape_dimension,bubble_colour)
if show_cntpt==1:
    imgoutput=imgfunc.DrawCentrePoint(imgoutput,mod_matrix_grid,cntpt_colour)


#---------------------------------------------------------------------------------------------


print "----------------------------------------"


#initialise plot
plt.subplot(111),plt.imshow(imgoutput)
plt.title('dilate1 Image'), plt.xticks([]), plt.yticks([])


plt.show()
cv2.waitKey(0)



