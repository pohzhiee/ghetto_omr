import numpy as np
import cv2
from edcamcam_testfile_shape import shapedetector
import matplotlib.pyplot as plt

#Part 1: Image Loading
#-------------------------------------------------------------------
#load image
img2= cv2.imread('img_data/omstest1.jpg')

#bilateral filter, sharpen, thresh
biblur=cv2.bilateralFilter(img,20,175,175)
sharp=cv2.addWeighted(img,1.55,biblur,-0.5,0)
ret1,thresh1 = cv2.threshold(sharp,127,255,cv2.THRESH_OTSU)

#negative image
inv=cv2.bitwise_not(thresh1)

#closed image
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
closed = cv2.morphologyEx(inv, cv2.MORPH_CLOSE, kernel)


#Part 2: Finding Valid Contours
#-------------------------------------------------------------------
#find countours
im2, contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


#prepare empty canvas
height, width = img.shape[:2]
emptycanvas=np.zeros((height,width),dtype=np.uint8)

#truncate contours with A<10
kcounter = 0
for c in contours:

    A = cv2.contourArea(c)

    if A<100:
        contours=np.delete(contours,kcounter,0)
        kcounter=kcounter-1
    kcounter=kcounter+1

#find length of contour array
clen=len(contours)

#create match_array [dimension = len x len] with 0s
match_array=np.zeros((clen,clen),np.uint8)

#loop over the contours and compare two by two
icounter = 0
for i in contours:
    jcounter = 0

    for j in contours:
    #If difference has index <0.01 then regard as TRUE
        ret=cv2.matchShapes(i,j,1,0.0)
        if ret<0.01:
            match_array[icounter,jcounter]=1
        else:
            match_array[icounter,jcounter]=0
        jcounter=jcounter+1
    icounter=icounter+1


#sum each row of the array (for TRUEs and FALSEs]
sum_array=np.sum(match_array,axis=1,dtype=np.int32)
print len(sum_array)
#finding mean of the comparison value
sum_array2=np.sum(sum_array,axis=0,dtype=np.int32)
sum_array_len=len(sum_array)
ave_sim_val=sum_array2/sum_array_len

#counters
#creation of new array to store centre point
#variables
counter_a=0
counter_s=0
counter_m=0
random_counter =0
centpt_array = np.array([[0,0,0]])
Sum_A=0

#find valid mean area
for k in sum_array:
    if k>ave_sim_val:
        A = cv2.contourArea(contours[counter_s])
        Sum_A=Sum_A+A
        counter_a=counter_a+1
    counter_s=counter_s +1
mean_valid_A=Sum_A/counter_a


#find midpoints of contours that fulfils 1)high similarity 2)occurence greater than average 3)deviation from valid median area
for i in sum_array:

    if i>ave_sim_val:

        cv2.drawContours(img2, contours, counter_m, (0, 255, 0), 2)

        #obtain centre point of each contour
        M=cv2.moments(contours[counter_m])
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])

        #Determine valid mean area
        if cv2.contourArea(contours[counter_m])>mean_valid_A:
            cA=cv2.contourArea(contours[counter_m])
            new_centpt_array=np.array([[cX,cY,cA]])
            centpt_array=np.concatenate((centpt_array,new_centpt_array),axis=0)
            random_counter = random_counter +1
    counter_m = counter_m+1

##checkpoint
print '-----------'
print random_counter
print len(centpt_array)

#delete 1st row
centpt_array=np.delete(centpt_array,0,0)
print centpt_array

#initialise plot
plt.subplot(111),plt.imshow(img2)
plt.title('dilate1 Image'), plt.xticks([]), plt.yticks([])
for k in centpt_array:
    plt.plot(k[0],k[1],'ro')


plt.show()

cv2.waitKey(0)


