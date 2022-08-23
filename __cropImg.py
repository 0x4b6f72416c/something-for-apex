import cv2 
import numpy as np


x,y,h,w = 3545,50,40,60


for i in range(2,21):
    image = cv2.imread(f"imgTocrop/{i}.png")

    crop = image[y:y+h,x:x+w]
    #canny = cv2.Canny(crop,50,100)
    cv2.imwrite(f"cropedImg/{i}.png",crop)
