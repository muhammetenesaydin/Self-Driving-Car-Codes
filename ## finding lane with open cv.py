#####finding lane with open cv######## 
import cv2
import numpy as np
import matplotlib.pyplot as plt

def Canny(img ):
    gray = cv2.cvtColor(imgg,cv2.COLOR_BGR2GRAY)    
    blur=cv2.GaussianBlur(gray,(5,5),0) 
    canny=cv2.Canny(blur,50,150)
    return canny
def region_of_interest(img):
    height=img.shape[0]
    polygons=np.array([[(200,height),(1100,height),(550,250)]])
    mask=np.zeros_like(img)
    cv2.fillPoly(mask,polygons,255)
    masked_image=cv2.bitwise_and(img,mask)
    return masked_image

img = cv2.imread ('test_image.jpg')
lane = np.copy(img)
imgg= np.copy(img)
img=region_of_interest(img)
canny =Canny(img) 
cropped= region_of_interest(canny)    
cv2.imshow("result",region_of_interest(canny))
cv2.waitKey(0)
