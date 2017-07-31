import cv2
import numpy as np

#Settings:
path='img_data/omstest2.jpg'


#Global settings
drawing = False #Drawing Function: True if mouse is pressed
ix,iy = 0,0 #Initial Coordinate True if mouse is pressed
layer_data=np.zeros([1,3],dtype=np.ndarray)
print layer_data

# mouse callback function
def draw_rectangle(event,x,y,flags,param):
    global ix,iy,drawing,mode,layer_data

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            a=layering()
            img_temp_rect=a.copy()
            img_temp_rect=cv2.rectangle(img_temp_rect,(ix,iy),(x,y),(0,255,0),2)
            cv2.imshow('image',img_temp_rect)


    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        shape_dimension1 = np.asarray((ix,iy))
        shape_dimension2=np.asarray((x,y))

        layer_data.resize(layer_data.shape[0]+1,3)

        k = layer_data.shape
        layer_data[k[0]-1, 0] = 1
        layer_data[k[0]-1, 1] = shape_dimension1
        layer_data[k[0]-1, 2] = shape_dimension2
        print layer_data
        a=layering()

def layering():
    global layer_data
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
cv2.setMouseCallback('image',draw_rectangle)




while(1):
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break

cv2.destroyAllWindows()