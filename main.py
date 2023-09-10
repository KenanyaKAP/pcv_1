import cv2
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

img = cv2.imread('image2.jpg')
brightness = 0
contrast = 0
saturation = 0

fig, axs = plt.subplots(2, 2)
fig.suptitle('Histogram')

def updateImage():
    # Container
    imgUpdate = img.astype(np.double)

    # Contrast
    imgUpdate = np.clip(((.006*contrast+1) if contrast <= 0 else (.04*contrast+1))*(imgUpdate-128)+128, 0, 255)

    # Brightness
    imgUpdate = np.clip(imgUpdate+brightness, 0, 255)

    # Saturation
    imgSat = (imgUpdate[:,:,0] + imgUpdate[:,:,1] + imgUpdate[:,:,2])/3
    lerpT = (saturation+100)/100
    imgUpdate[:,:,0] = imgSat*(1-lerpT) + imgUpdate[:,:,0]*lerpT
    imgUpdate[:,:,1] = imgSat*(1-lerpT) + imgUpdate[:,:,1]*lerpT
    imgUpdate[:,:,2] = imgSat*(1-lerpT) + imgUpdate[:,:,2]*lerpT
    imgUpdate = np.clip(imgUpdate, 0, 255)

    # Create Histogram
    histrGs = cv2.calcHist([imgSat.astype(np.uint8)],[0],None,[256],[0,256])
    histrB = cv2.calcHist([imgUpdate[:,:,0].astype(np.uint8)],[0],None,[256],[0,256])
    histrG = cv2.calcHist([imgUpdate[:,:,1].astype(np.uint8)],[0],None,[256],[0,256])
    histrR = cv2.calcHist([imgUpdate[:,:,2].astype(np.uint8)],[0],None,[256],[0,256])
    
    # Plot Grayscale
    axs[0, 0].cla()
    axs[0, 0].set_title('Grayscale')
    axs[0, 0].fill_between(np.arange(histrGs.shape[0]), histrGs.reshape(-1), color='gray')
    
    # Plot Blue
    axs[0, 1].cla()
    axs[0, 1].set_title('Blue')
    axs[0, 1].fill_between(np.arange(histrB.shape[0]), histrB.reshape(-1), color='blue')
    
    # Plot Green
    axs[1, 0].cla()
    axs[1, 0].set_title('Green')
    axs[1, 0].fill_between(np.arange(histrG.shape[0]), histrG.reshape(-1), color='green')
    
    # Plot Red
    axs[1, 1].cla()
    axs[1, 1].set_title('Red')
    axs[1, 1].fill_between(np.arange(histrR.shape[0]), histrR.reshape(-1), color='red')

    # Show image
    imgUpdate /= 255
    cv2.imshow('Image', imgUpdate)
    
    # Convert histogram canvas to image and show
    fig.canvas.draw()
    histoImg = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    histoImg  = histoImg.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    histoImg = cv2.cvtColor(histoImg,cv2.COLOR_RGB2BGR)
    cv2.imshow("Histogram",histoImg)

def changeBrightness(value):
    global brightness
    brightness = value
    updateImage()

def changeContrast(value):
    global contrast
    contrast = value
    updateImage()

def changeSaturation(value):
    global saturation
    saturation = value
    updateImage()

updateImage()

cv2.createTrackbar('Brightness', 'Image', 0, 100, lambda x: changeBrightness(x))
cv2.setTrackbarMin('Brightness', 'Image', -100)

cv2.createTrackbar('Contrast', 'Image', 0, 100, lambda x: changeContrast(x))
cv2.setTrackbarMin('Contrast', 'Image', -100)

cv2.createTrackbar('Saturation', 'Image', 0, 100, lambda x: changeSaturation(x))
cv2.setTrackbarMin('Saturation', 'Image', -100)

while 1:
    k = cv2.waitKey(33) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()