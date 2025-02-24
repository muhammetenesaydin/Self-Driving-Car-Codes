import cv2 
import numpy as np
import matplotlib.pyplot as plt

image=cv2.imread('test_image.jpg')
lane_image=np.copy (image)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  
blur=cv2.GaussianBlur(gray,(5,5),0)
canny=cv2.Canny(gray,50,150)
cv2.imshow("result",image)
cv2.waitKey(0)
