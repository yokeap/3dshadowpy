import cv2
import numpy as np
from skimage.morphology import skeletonize
from src import mathTools
from src import segmentation
import matplotlib.pyplot as plt

imgSample = cv2.imread('./test/test.jpg')
# imgSample = cv2.imread('./capture/2021-11-25 015652.342325/imgraw.jpg')
cv2.imshow("Image Input", imgSample)
# test hsv histogram plot
# imgSample = np.float32(imgSample)
imageHSV = cv2.cvtColor(imgSample, cv2.COLOR_BGR2HSV_FULL)
h, s, v = imageHSV[:,:,0], imageHSV[:,:,1], imageHSV[:,:,2]
hist_h = cv2.calcHist([h],[0],None,[360],[0,360])
hist_s = cv2.calcHist([s],[0],None,[256],[0,256])
hist_v = cv2.calcHist([v],[0],None,[256],[0,256])

print(hist_h[1])

# plt.plot(hist_h, color='r', label="h")
plt.plot(hist_s, color='g', label="s")
# plt.plot(hist_v, color='b', label="v")
plt.legend()
plt.show()


