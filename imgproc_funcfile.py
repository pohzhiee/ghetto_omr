import cv2
import numpy as np

def outlining(img):
    #bilateral filter, sharpen, thresh image
    biblur=cv2.bilateralFilter(img,20,175,175)
    sharp=cv2.addWeighted(img,1.55,biblur,-0.5,0)
    ret1,thresh1 = cv2.threshold(sharp,127,255,cv2.THRESH_OTSU)

    #negative and closed image
    inv=cv2.bitwise_not(thresh1)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    closed = cv2.morphologyEx(inv, cv2.MORPH_CLOSE, kernel)
    return closed

def contouring(img):
    #Defining coefficients
    #----------------------------------
    #Max value of contour shape matching coefficient
    match_coeff = 0.01
    #max contour area
    max_cont_area = 100
    #----------------------------------
    #find countours
    im2, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #truncate contours less than predefined maximum area
    c_counter = 0
    for c in contours:

        A = cv2.contourArea(c)

        if A<max_cont_area:
            contours=np.delete(contours,c_counter,0)
            c_counter=c_counter-1
        c_counter=c_counter+1

    #length of truncated contour array
    clen=c_counter

    #create match_array [dimension = len x len] with 0s
    match_array=np.zeros((clen,clen),np.uint8)

    #loop over the contours and compare two by two
    icounter = 0
    for i in contours:
        jcounter = 0

        for j in contours:
        #If difference has index <0.01 then regard as TRUE
            ret=cv2.matchShapes(i,j,1,0.0)
            if ret<match_coeff:
                match_array[icounter,jcounter]=1
            else:
                match_array[icounter,jcounter]=0
            jcounter=jcounter+1
        icounter=icounter+1


    #sum each row of the array (for TRUEs and FALSEs]
    sum_array=np.sum(match_array,axis=1,dtype=np.uint16)
    #finding mean of the comparison value
    sum_all=np.sum(sum_array,axis=0,dtype=np.uint16)
    ave_sim_val=sum_all/clen
    #Assumption: there is a lot of 1s
    return contours,sum_array,ave_sim_val

def shape_detector(contours,hor_dist,ver_dist):
    shape_dimension_matr = np.zeros((len(contours), 2), dtype=np.ndarray)
    m=0
    for c in contours:
        M = cv2.moments(c)
        while m < len(contours):
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            asp_ratio = float(hor_dist) /float(ver_dist)

            # if the shape has 4 vertices, it is either a square or a rectangle
            if len(approx) == 4:
                shape = 1 #1:rectangle or square
                # compute the bounding box of the contour
                (x, y, w, h) = cv2.boundingRect(c)
                shape_dimension=w,h

            # otherwise, we assume the shape is a circle or oval
            else:
                #differentiate them using aspect ratio
                if 0.95<asp_ratio<1.05:
                     shape = 2 #2:circle
                     # compute the bounding circle of the contour
                     (x, y), r = cv2.minEnclosingCircle(c)
                     shape_dimension = r
                else:
                    shape=3 #3:oval
                    # compute the bounding ellipse of the contour
                    (x, y), (MA, ma), angle= cv2.fitEllipse(c)
                    shape_dimension = MA,ma

            shape_dimension_matr[m,0]=shape
            shape_dimension_matr[m, 1] =shape_dimension
            m=m+1

        else:
            shape = 0
            shape_dimension = 0
            asp_ratio=0


    shape_dimension_matr_mod=np.compress([1,0],shape_dimension_matr,axis=1)
    shape_index_sum=shape_dimension_matr_mod.sum(axis=1)
    shape_index_sum_diff=np.ediff1d(shape_index_sum)

    if np.any(shape_index_sum_diff)!=0:
         print 'Error'


    elif np.all(shape_index_sum_diff)==0:
        shape_dimension_matr_mod2 = np.compress([0, 1], shape_dimension_matr, axis=1)

        sum_para_1 = 0
        sum_para_2 = 0

        if shape_index_sum[0]==2:
            shape_dimension_para= shape_dimension_matr_mod2.sum(axis=0)/shape_dimension_matr_mod2.shape[0]

        elif shape_index_sum[0]==1 or 3:
            h=0
            while h<shape_dimension_matr_mod2.shape[0]:
                h_var=shape_dimension_matr_mod2[h]
                h_var2=[list(x)for x in h_var]
                h_var3=h_var2[0]
                sum_para_1=sum_para_1+h_var3[0]
                h=h+1
            para_1=sum_para_1/shape_dimension_matr_mod2.shape[0]

            g = 0
            while g < shape_dimension_matr_mod2.shape[0]:
                g_var = shape_dimension_matr_mod2[g]
                g_var2 = [list(x) for x in g_var]
                g_var3=g_var2[0]
                sum_para_2 = sum_para_2 + g_var3[1]
                g = g + 1
            para_2 = sum_para_2 / shape_dimension_matr_mod2.shape[0]

            shape_dimension_para=[para_1,para_2]

        return shape_index_sum[0],shape_dimension_para


def get_centre(contours,sum_array,ave_sim_val):
    #counters
    #creation of new array to store centre point
    #variables
    counter_a=0
    counter_s=0
    counter_m=0
    valid_counter =0
    centpt_array = np.array([[0,0,0]])

    hor_dist_acc=0
    ver_dist_acc=0

    #Area array
    area_arr=np.array([])

    #find valid mean area and SD
    for k in sum_array:
        if k>ave_sim_val:
            A = cv2.contourArea(contours[counter_s])
            area_arr=np.append(area_arr,[A],0)
            counter_a=counter_a+1
        counter_s=counter_s +1

    sum_area_array=np.array([])
    sum_area_array=np.sum(area_arr,axis=0,dtype=np.uint32)
    mean_valid_A=sum_area_array/counter_a
    sum_dif=0

    for a in area_arr:
        dif = (mean_valid_A - a)**2
        sum_dif=sum_dif+dif
    SD_valid=(sum_dif/counter_a)**0.5

    #find midpoints of contours that fulfils 1)high similarity 2)occurence greater than average 3)least deviation from valid mean area
    for i in sum_array:

        if i>ave_sim_val:

            #Determine valid mean area, taken to be within 2 standard deviation of areas
            condition = cv2.contourArea(contours[counter_m])>mean_valid_A-2*SD_valid and cv2.contourArea(contours[counter_m])<mean_valid_A+2*SD_valid
            if condition:

                # obtain centre point of each contour
                M = cv2.moments(contours[counter_m])
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])

                # store in it arrays
                new_centpt_array=np.array([[cX,cY,counter_m]])
                centpt_array=np.concatenate((centpt_array,new_centpt_array),axis=0)

                #determine horizontal point and vertical point
                c=contours[counter_m]
                Xt_right=np.asarray(tuple(c[c[:,:,0].argmax()][0]))
                Xt_bot=np.asarray(tuple(c[c[:,:,1].argmax()][0]))

                hor_dist=Xt_right[0]-cX
                ver_dist=Xt_bot[1]-cY
                hor_dist_acc=hor_dist_acc+hor_dist
                ver_dist_acc=ver_dist_acc+ver_dist

                valid_counter = valid_counter +1

        counter_m = counter_m+1

    mean_hor_dist=hor_dist_acc/valid_counter
    mean_ver_dist=ver_dist_acc/valid_counter

    #delete 1st row
    centpt_array=np.delete(centpt_array,0,0)

    #select contours number (into an array) to run shape detector
    sel_cont_num=np.array([0])
    len(centpt_array)
    j=0
    while j<len(centpt_array):
        position=centpt_array[j]
        sel_cont_num=np.append(sel_cont_num,[position[2]],0)
        j=j+1
    sel_cont_num = np.delete(sel_cont_num, 0, 0)

    #using the contours number position create a binary (which is the compress criteria)
    compress_criteria=np.zeros(len(contours),dtype=np.uint8)
    for c in sel_cont_num:
        compress_criteria[c]=1

    #compress/truncate unwanted contours as contours_modified
    contours_mod=np.compress(compress_criteria,contours,0)
    # run shape_detector to determine the dimension of shape
    shape_type,shape_dimension = shape_detector(contours_mod, mean_hor_dist, mean_ver_dist)

    ##checkpoint for adding array (Remove it in actual program)
    centpt_array=np.append(centpt_array,[[100,100,1000]],0)
    centpt_array=np.append(centpt_array,[[40,290,1001]],0)
    centpt_array=np.append(centpt_array,[[450,800,1002]],0)
    centpt_array=np.append(centpt_array,[[100,300,1003]],0)
    centpt_array=np.append(centpt_array,[[0,0,1004]],0)

    #Removing Duplicates
    g=0
    arr_len=len(centpt_array)

    while arr_len>g:
        target_arr1 = centpt_array[g]
        h=1+g
        while arr_len>h and h>g:
            target_arr2 = centpt_array[h]

            if abs(target_arr1[0]-target_arr2[0])<mean_hor_dist:
                if abs(target_arr1[1]-target_arr2[1])<mean_ver_dist:
                    centpt_array=np.delete(centpt_array,h,0)
                    h=h-1
                    arr_len=arr_len-1
            h = h + 1
        g=g+1

    return centpt_array,mean_hor_dist,mean_ver_dist,shape_type, shape_dimension

#form grid function

def formgrid(centpt_array,mean_hor_dist,mean_ver_dist):
#Scanning center point x and y and sort
    cX_array=np.array([])
    cY_array=np.array([])

    for k in centpt_array:
        cX_array = np.append(cX_array, [k[0]], 0)
        cX_array=np.sort(cX_array,axis=0,kind='mergesort')
        cY_array = np.append(cY_array, [k[1]], 0)
        cY_array = np.sort(cY_array, axis=0, kind='mergesort')


    #group the sorted array of x and y
    g = 0
    temp_var_counter=0
    grp_cX_array=np.array([])
    temp_var =0

    while g < len(cX_array):
        if g==0:
            temp_var=cX_array[g]
            temp_var_counter=1

        elif cX_array[g]-cX_array[g-1]<mean_hor_dist:
            if g == len(cX_array) - 1:
                temp_var = temp_var + cX_array[g]
                temp_var_counter = temp_var_counter + 1
                temp_var_ave = temp_var / temp_var_counter
                grp_cX_array = np.append(grp_cX_array, [temp_var_ave], 0)
                temp_var = 0
                temp_var_counter = 0
            else:
                temp_var=temp_var+cX_array[g]
                temp_var_counter=temp_var_counter+1

        elif cX_array[g]-cX_array[g-1]>mean_hor_dist:
            if g == len(cX_array) - 1:
                temp_var=temp_var+cX_array[g-1]
                temp_var_counter=temp_var_counter+1
                temp_var_ave = temp_var / temp_var_counter
                grp_cX_array = np.append(grp_cX_array, [temp_var_ave], 0)
                temp_var = cX_array[g]
                temp_var_counter = 1
                temp_var_ave = temp_var / temp_var_counter
                grp_cX_array = np.append(grp_cX_array, [temp_var_ave], 0)
                temp_var = 0
                temp_var_counter = 0
            else:
                temp_var_ave=temp_var/temp_var_counter
                grp_cX_array = np.append(grp_cX_array,[temp_var_ave],0)
                temp_var=cX_array[g]
                temp_var_counter=1
        g=g+1

    h = 0
    temp_var_counter=0
    grp_cY_array=np.array([])
    while h < len(cY_array):
        if h==0:
            temp_var=cY_array[h]
            temp_var_counter=1



        elif cY_array[h]-cY_array[h-1]<mean_ver_dist:
            if h == len(cY_array) - 1:
                temp_var = temp_var + cY_array[h]
                temp_var_counter = temp_var_counter + 1
                temp_var_ave = temp_var / temp_var_counter
                grp_cY_array = np.append(grp_cY_array, [temp_var_ave], 0)
                temp_var = 0
                temp_var_counter = 0
            else:
                temp_var=temp_var+cY_array[h]
                temp_var_counter=temp_var_counter+1

        elif cY_array[h]-cY_array[h-1]>mean_ver_dist:
            if h == len(cY_array) - 1:
                temp_var=temp_var+cY_array[h-1]
                temp_var_counter=temp_var_counter+1
                temp_var_ave = temp_var / temp_var_counter
                grp_cY_array = np.append(grp_cY_array, [temp_var_ave], 0)
                temp_var = cY_array[h]
                temp_var_counter = 1
                temp_var_ave = temp_var / temp_var_counter
                grp_cY_array = np.append(grp_cY_array, [temp_var_ave], 0)
                temp_var = 0
                temp_var_counter = 0
            else:
                temp_var_ave=temp_var/temp_var_counter
                grp_cY_array = np.append(grp_cY_array,[temp_var_ave],0)
                temp_var=cY_array[h]
                temp_var_counter=1
        h=h+1



    #set up grid m x n
    grid_row_len=len(grp_cY_array)
    grid_col_len=len(grp_cX_array)

    matrix_grid=np.zeros((grid_row_len,grid_col_len),dtype=np.ndarray)

    #fill in the grid
    for k in centpt_array:
        p=0
        while p < grid_col_len:
            if k[0]<grp_cX_array[p]+mean_hor_dist and k[0]>grp_cX_array[p]-mean_hor_dist:

                q=0
                while q<grid_row_len:
                    if k[1]<grp_cY_array[q]+mean_ver_dist and k[1]>grp_cY_array[q]-mean_ver_dist:
                        matrix_grid[q,p]=k
                    q=q+1
            p=p+1
    return matrix_grid

#function to find all the x and y coordinate of the matrix grid
def MatrArrFunc(matr):
    matr_shape = matr.shape
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

    return val_X_array, val_Y_array

#function to check spacing of matrix (difference between x and y)
def SpaceFunc(val_x_array,val_y_array):
    spa_X_array = np.ediff1d(val_x_array)
    spa_Y_array = np.ediff1d(val_y_array)

    return spa_X_array,spa_Y_array

#Fucntion to convert matrix to binary (those with value to 1, those with 0 to 0)
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
        print "Error:No. of Rows Incorrect"
    if n_col != np.sum(compress_criteria_col):
        print "Error:No. of Columns Incorrect"


    opt_matr_init =np.compress(compress_criteria_row,matrix_grid,axis=0)
    opt_matr = np.compress(compress_criteria_col, opt_matr_init, axis=1)

    #Checking Spacing Regularity, otherwise return error
    #If Spacing are regular, fill up missing centere points
    val_x_arr,val_y_arr=MatrArrFunc(opt_matr)
    spa_x_arr,spa_y_arr=SpaceFunc(val_x_arr,val_y_arr)

    spa_x_diff = np.ediff1d(spa_x_arr)
    spa_y_diff = np.ediff1d(spa_y_arr)
    if abs(np.any(spa_x_diff))>2 or abs(np.any(spa_y_diff))>2:
        print 'Error:Optimisation M'
    else:
        opt_bin_matr_init = np.compress(compress_criteria_row, bin_matr, axis=0)
        opt_bin_matr = np.compress(compress_criteria_col, opt_bin_matr_init, axis=1)

        row_index=0
        while row_index<opt_bin_matr.shape[0]:
            col_index=0
            while col_index<opt_bin_matr.shape[1]:
                if opt_bin_matr[row_index,col_index]==0:
                    opt_matr[row_index,col_index]=[val_x_arr[col_index],val_y_arr[row_index],0]
                col_index=col_index+1
            row_index=row_index+1

    return opt_matr

def ModMatrGrid(matr):
    matr = matr.reshape(matr.shape[0] * matr.shape[1])
    mod_matr = np.zeros((matr.shape[0], 3), dtype=np.uint32)
    k = 0
    while k < matr.shape[0]:
        g = matr[k]
        mod_matr[k, 0] = g[0]
        mod_matr[k, 1] = g[1]
        mod_matr[k, 2] = g[2]
        k = k + 1
    return mod_matr

def DrawShape(img,matr,shape_type,shape_dimension,bubble_colour,bubble_linethickness):
    if shape_type==1: #1=rectangle/square
        for k in matr:
            imgoutput=cv2.rectangle(img,(k[0],k[1]),(k[0]+shape_dimension[0],k[1]+shape_dimension[1]),bubble_colour,bubble_linethickness)
    elif shape_type==2: #2=circle
        for k in matr:
            imgoutput=cv2.circle(img,(k[0],k[1]),int(shape_dimension[0]),bubble_colour,bubble_linethickness)
    elif shape_type == 3:  # 2=oval
        for k in matr:
            imgoutput = cv2.ellipse(img, ((k[0], k[1]), (shape_dimension[0], shape_dimension[1]), 0), bubble_colour, bubble_linethickness)

    return imgoutput

def DrawCentrePoint(img,matr,cntpt_colour,cntpt_size):
    for k in matr:
        imgoutput = cv2.circle(img, (k[0], k[1]),cntpt_size,cntpt_colour, -1)
    return imgoutput

