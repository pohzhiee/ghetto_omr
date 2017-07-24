import numpy as np
import cv2
img = cv2.imread('img_data/oms2.jpg',cv2.IMREAD_GRAYSCALE)
biblur=cv2.bilateralFilter(img,20,175,175)
sharp=cv2.addWeighted(img,1.55,biblur,-0.5,0)
ret1,thresh1 = cv2.threshold(sharp,127,255,cv2.THRESH_OTSU)
height, width = img.shape[:2]

inv=cv2.bitwise_not(thresh1)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
closed = cv2.morphologyEx(inv, cv2.MORPH_CLOSE, kernel)


im2, contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
empt=np.zeros((height,width),dtype=np.uint8)
cv2.imshow("thresh1",thresh1)
cv2.imshow("CLOSED",closed)
cv2.drawContours(empt, contours, -1, (255,255,255), 3)

im3,contours1,hierarchy1 = cv2.findContours(empt, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
empt1=np.zeros((height,width),dtype=np.uint8)
cv2.imshow("CONTOUR",empt)
cv2.drawContours(empt1, contours1, -1, (255,255,255), 3)
cv2.imshow("CONTOUR1",empt1)
cv2.waitKey(0)

