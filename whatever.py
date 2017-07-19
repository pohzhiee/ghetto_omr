import cv2
import numpy as np
from matplotlib import pyplot as plt
import img_func
import matplotlib
img = cv2.imread('img_data/oms1.jpg',0)
edges = cv2.Canny(img,200,255)
thresh, blurred = img_func.thres1(edges)
kernel = np.ones((2,2),np.uint8)
dilated1 = cv2.dilate(thresh,kernel,iterations=3)
blur_dil1 = cv2.GaussianBlur(dilated1,(5,5),0)
ero1 = cv2.erode(blur_dil1,kernel,iterations=3)
dilated2 = cv2.dilate(img,kernel,iterations=1)
edge2 = cv2.Canny(img,200,255)
plt.subplot(231),plt.imshow(edges,cmap = 'gray')
plt.title('edge1 Image'), plt.xticks([]), plt.yticks([])
plt.subplot(232),plt.imshow(dilated1,cmap = 'gray')
plt.title('dilate1 Image'), plt.xticks([]), plt.yticks([])
plt.subplot(233),plt.imshow(blur_dil1,cmap = 'gray')
plt.title('dilate1 Image'), plt.xticks([]), plt.yticks([])
plt.subplot(234),plt.imshow(ero1,cmap = 'gray')
plt.title('dilate2 Image'), plt.xticks([]), plt.yticks([])
plt.subplot(235),plt.imshow(edge2,cmap = 'gray')
plt.title('edge2 Image'), plt.xticks([]), plt.yticks([])
plt.show()
