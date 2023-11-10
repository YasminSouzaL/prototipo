#optical mark recognition (omr) MCQ Automated Grading - OpenCV with Python
import cv2
import numpy as np
import utis
###################################
path = 'test.jpg'
widhtImg = 700
heightImg = 700
###################################
img = cv2.imread(path)

#Preprocessing
img = cv2.resize(img, (widhtImg, heightImg))
imgContours = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
imgCanny = cv2.Canny(imgBlur, 10, 50)
 
#Find Contours
countours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgContours, countours, -1, (0,255,0), 10)

#Find Rectangle
rectCon = utis.rectContour(countours)
biggestContour = utis.getCornerPoints(rectCon[0])

imgBlank = np.zeros_like(img)
imageArray = ([img, imgGray, imgBlur, imgCanny],
              [imgContours, imgBlank, imgBlank, imgBlank])

imgStack = utis.stackImages(imageArray, 0.5) 

cv2.imshow("ImageStack", imgStack)
cv2.waitKey(0)
