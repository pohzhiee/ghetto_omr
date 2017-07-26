import numpy as np
import cv2
import matplotlib.pyplot as plt


img = cv2.imread('img_data/omstest1b.jpg',cv2.IMREAD_GRAYSCALE)
img2= cv2.imread('img_data/omstest1b.jpg')
img3=cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

biblur=cv2.bilateralFilter(img,20,175,175)
sharp=cv2.addWeighted(img,1.55,biblur,-0.5,0)
ret1,thresh1 = cv2.threshold(sharp,127,255,cv2.THRESH_OTSU)

# Create SURF object. You can specify params here or later.
# Here I set Hessian Threshold to 400

k=100000
while k >0:
    surf = cv2.xfeatures2d.SURF_create(k)

    # Find keypoints and descriptors directly
    kp, des = surf.detectAndCompute(img,None)
    print len(kp)
    if len(kp)>100:
        break
    k=k-10000

imga1 = cv2.drawKeypoints(thresh1,kp,None,(255,0,0),4)
plt.imshow(imga1),plt.show()
