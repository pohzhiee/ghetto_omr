import numpy as np
import cv2
from edcamcam_testfile_shape import shapedetector
import matplotlib.pyplot as plt


#load image
img = cv2.imread('img_data/omstest1.jpg',cv2.IMREAD_GRAYSCALE)
img2= cv2.imread('img_data/omstest1.jpg')

#bilateral filter, sharpen, thresh
biblur=cv2.bilateralFilter(img,20,175,175)
sharp=cv2.addWeighted(img,1.55,biblur,-0.5,0)
ret1,thresh1 = cv2.threshold(sharp,127,255,cv2.THRESH_OTSU)

#negative image
inv=cv2.bitwise_not(thresh1)

#closed image
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
closed = cv2.morphologyEx(inv, cv2.MORPH_CLOSE, kernel)

#find countours
im2, contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


#prepare empty canvas
height, width = img.shape[:2]
emptycanvas=np.zeros((height,width),dtype=np.uint8)

kcounter = 0
for c in contours:

    A = cv2.contourArea(c)

    if A<200:
        contours=np.delete(contours,kcounter,0)
        kcounter=kcounter-1
    kcounter=kcounter+1


clen=len(contours)
print clen
matcharray=np.zeros((clen,clen),np.uint8)


#loop over the contours
icounter = 0
for i in contours:
    jcounter = 0

    for j in contours:
    #Storing data in an array
        ret=cv2.matchShapes(i,j,1,0.0)
        if ret<0.01:
            matcharray[icounter,jcounter]=1
        else:
            matcharray[icounter,jcounter]=0
        jcounter=jcounter+1
    icounter=icounter+1

print matcharray
sum_array=np.sum(matcharray,axis=1,dtype=np.int32)
print sum_array
counter_m=0
n_true =0
for i in sum_array:
    print i
    if i>1:
        cv2.drawContours(img2, contours, counter_m, (0, 255, 0), 2)
        n_true = n_true +1
    counter_m = counter_m+1
print '-----------'
print n_true
cv2.imshow("IMG",img2)
cv2.waitKey(0)


