def bin_mat(n_row,n_col,dec_num):
    import numpy as np
    import itertools
    num_bits = n_row*n_col
    if dec_num<num_bits:
        matr = np.empty((n_row,n_col),np.uint8)
        str1 = "{0:0" + str(num_bits) + "b}"
        bin_num = str1.format(dec_num)
        row_count=0;
        count=0;
        for row in matr:
            col_count=0
            for col in row:
                matr[row_count,col_count]=bin_num[count]
                count=count+1
                col_count=col_count+1
            row_count=row_count+1
    return matr