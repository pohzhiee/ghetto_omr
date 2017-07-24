import numpy as np
import cv2
img = cv2.imread('img_data/oms1.jpg',cv2.IMREAD_GRAYSCALE)
biblur=cv2.bilateralFilter(img,20,175,175)
sharp=cv2.addWeighted(img,1.55,biblur,-0.5,0)
ret1,thresh1 = cv2.threshold(sharp,127,255,cv2.THRESH_OTSU)
height, width = img.shape[:2]
im2, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
empt=np.zeros((height,width),dtype=np.uint8)
cv2.imshow("thresh1",thresh1)
cv2.imshow("IM2",im2)
cv2.drawContours(empt, contours, -1, (255,255,255), 3)
cv2.imshow("CONTOUR",empt)
cv2.waitKey(0)
