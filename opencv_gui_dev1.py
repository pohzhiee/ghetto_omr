import cv2
import numpy as np

#Settings:
path='img_data/omstest2.jpg'


class data:
    def __init__(self):
        self.layer_data =np.zeros([1,4],dtype=np.ndarray)
        self.layer_index = 0
        self.ix,self.iy=0,0
        self.drawing = False
    def setxy(self,x,y):
        self.ix = x
        self.iy = y
    def printxy(self):
        print self.ix
        print self.iy

def draw_rectangle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        param.drawing=True
        param.setxy(x,y)
        param.printxy()

    elif event == cv2.EVENT_MOUSEMOVE:
        if param.drawing == True:
            a=layering(param.layer_data,param.layer_index)
            img_temp_rect=a.copy()
            img_temp_rect=cv2.rectangle(img_temp_rect,(param.ix,param.iy),(x,y),(0,255,0),2)
            cv2.imshow('image',img_temp_rect)


    elif event == cv2.EVENT_LBUTTONUP:
        param.drawing = False
        shape_dimension1 = np.asarray((param.ix,param.iy))
        shape_dimension2=np.asarray((x,y))

        param.layer_data.resize(param.layer_data.shape[0]+1,4)

        k = param.layer_data.shape
        param.layer_data[k[0]-1, 0] = 1
        param.layer_data[k[0]-1, 1] = shape_dimension1
        param.layer_data[k[0]-1, 2] = shape_dimension2
        param.layer_data[k[0]-1,3]=param.layer_index+1
        param.layer_index=param.layer_index+1
        print param.layer_data
        a=layering(param.layer_data,param.layer_index)

def layering(layer_data,layer_index):
    img_output = img.copy()
    g=0
    while g<layer_data.shape[0]:
        if layer_data[g,0]==1:
            p=layer_data[g, 1]
            q=layer_data[g,2]
            img_output=cv2.rectangle(img_output,(p[0],p[1]),(q[0],q[1]),(255,255,0),2)
            img_output=img_output.copy()
        g=g+1

    cv2.imshow('image', img_output)
    return img_output

img=cv2.imread(path)
cv2.imshow('image', img)
cv2.namedWindow('image')
objdat = data()
cv2.setMouseCallback('image',draw_rectangle,objdat)




while(1):
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break

cv2.destroyAllWindows()