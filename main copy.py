import cv2
from matplotlib import pyplot as plt
import numpy as np

img = cv2.imread('image.jpg')
brightness = 0
contrast = [[0, 64, 192, 255], [0, 64, 192, 255]]
imgHistr = cv2.calcHist([img],[0],None,[256],[0,256])

def updateImage():
    global imgHistr, brightness, contrast

    imgUpdate = img.astype(np.double)
    imgUpdate += brightness
    
    imgUpdate[imgUpdate < contrast[0][1]] *= contrast[1][1] / contrast[0][1]
    imgUpdate[(imgUpdate >= contrast[0][1]) & (imgUpdate < contrast[0][2])] = (imgUpdate[(imgUpdate >= contrast[0][1]) & (imgUpdate < contrast[0][2])] - contrast[0][1]) * ((contrast[1][2]-contrast[1][1])/(contrast[0][2]-contrast[0][1])) + contrast[1][1]
    imgUpdate[imgUpdate >= contrast[0][2]] = (imgUpdate[imgUpdate >= contrast[0][2]] - contrast[0][2]) * ((255-contrast[1][2])/(255-contrast[0][2])) + contrast[1][2]
    
    imgUpdate /= 255
    cv2.imshow('Image', imgUpdate)

    imgUpdate[imgUpdate > 1] = 1
    imgUpdate[imgUpdate < 0] = 0

    imgHistrData = imgUpdate * 255
    imgHistrData = imgHistrData.astype(np.uint8)

    imgHistr = cv2.calcHist([imgHistrData],[0],None,[256],[0,256])

    plt.figure(0)
    plt.clf()
    plt.fill_between(np.arange(imgHistr.shape[0]), imgHistr.reshape(-1))
    plt.title('Histogram')
    plt.show(block=False)

    plt.figure(1)
    plt.clf()
    plt.plot(contrast[0], contrast[1])
    plt.title('Contras Function')
    plt.show(block=False)

def changeBrightness(value):
    global brightness
    brightness = value
    updateImage()

def changeContrast():
    pass

cv2.imshow('Image', img)

plt.figure(0)
plt.fill_between(np.arange(imgHistr.shape[0]), imgHistr.reshape(-1))
plt.title('Histogram')
plt.show(block=False)

plt.figure(1)
plt.clf()
plt.plot(contrast[0], contrast[1])
plt.title('Contras Function')
plt.show(block=False)

cv2.namedWindow('Control')
cv2.createTrackbar('Brightness', 'Control', 0, 255, lambda x: changeBrightness(x))
cv2.setTrackbarMin('Brightness', 'Control', -255)

def changeX1(x):
    contrast[0][1] = x
    updateImage()
def changeY1(x):
    contrast[1][1] = x
    updateImage()
def changeX2(x):
    contrast[0][2] = x
    updateImage()
def changeY2(x):
    contrast[1][2] = x
    updateImage()

cv2.createTrackbar('Contrast X1', 'Control', 64, 255, changeX1)
cv2.setTrackbarMin('Contrast X1', 'Control', 0)

cv2.createTrackbar('Contrast Y1', 'Control', 64, 255, changeY1)
cv2.setTrackbarMin('Contrast Y1', 'Control', 0)

cv2.createTrackbar('Contrast X2', 'Control', 192, 255, changeX2)
cv2.setTrackbarMin('Contrast X2', 'Control', 0)

cv2.createTrackbar('Contrast Y2', 'Control', 192, 255, changeY2)
cv2.setTrackbarMin('Contrast Y2', 'Control', 0)

cv2.waitKey(0)
cv2.destroyAllWindows()