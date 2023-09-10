import cv2
from matplotlib import pyplot as plt
import numpy as np 

############################################
# Program Utama
############################################    

# Membaca File  citra sebagai citra gray 
ImGray = cv2.imread("image.jpg",cv2.IMREAD_GRAYSCALE)
#############################################
#Menghitung histogram dengan fungsi calcHist
#############################################
Histogram = cv2.calcHist([ImGray],[0],None,[256],[0,256])
plt.bar(np.arange(0, 256, 1), Histogram[:, 0])
plt.show()
