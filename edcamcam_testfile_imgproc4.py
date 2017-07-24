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

x= np.array([])


#loop over the contours
for c in contours:

    #Storing areas in an array
    A = cv2.contourArea(c)
    x = np.append(x, [A], axis=0)



xsort=np.sort(x,axis=0,kind='mergesort')
xlen=len(xsort)

xmedian = xsort[xlen/2-1]
print xmedian
print xsort
print xlen

for c in contours:

    A = cv2.contourArea(c)
    if A<200:
        if A>100:
            cv2.drawContours(img2,[c],-1,(0,255,0),2)
            cv2.imshow("CONTOUR",img2)


plt.hist(xsort, [1,10,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500])
plt.show()

cv2.waitKey(0)

