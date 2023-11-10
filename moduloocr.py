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
imgBiggestContours = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
imgCanny = cv2.Canny(imgBlur, 10, 50)
 
#Find Contours
countours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgContours, countours, -1, (0,255,0), 10)

#Find Rectangle
rectCon = utis.rectContour(countours)
biggestContour = utis.getCornerPoints(rectCon[0])
gradePoints = utis.getCornerPoints(rectCon[1])

if biggestContour.size != 0 and gradePoints.size != 0:
    cv2.drawContours(imgBiggestContours, biggestContour, -1, (0,255,0), 20)
    cv2.drawContours(imgBiggestContours, gradePoints, -1, (255,0,0), 20)
    biggestContour=utis.reorder(biggestContour)
    gradePoints=utis.reorder(gradePoints)

    pt1 = np.float32(biggestContour)
    pt2 = np.float32([[0,0],[widhtImg,0],[0,heightImg],[widhtImg,heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (widhtImg, heightImg))

    ptG1 = np.float32(gradePoints)
    ptG2 = np.float32([[0,0],[325,0],[0,150],[325,150]])
    matrixG = cv2.getPerspectiveTransform(ptG1, ptG2)
    imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325,150))
    #cv2.imshow("Grade", imgGradeDisplay)

    #Apply Threshold
    imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgWarpGray, 170, 255, cv2.THRESH_BINARY_INV)[1]

    boxes = utis.splitBoxes(imgThresh)
    #cv2.imshow("Test", boxes[0])

    #Find the number of each box
    countR = 0
    countC = 0
    myPixelVal = np.zeros((questions, choices))
    
    for image in boxes:
        totalPixels = cv2.countNonZero(image)
        myPixelVal[countR][countC] = totalPixels
        countC += 1
        if (countC == choices):countR += 1; countC = 0

    #print(myPixelVal)
    myIndex = []
    for x in range (0, questions):
        arr = myPixelVal[x]
        #print('arr',arr)
        myIndexVal = np.where(arr == np.amax(arr))
        #print('myIndexVal',myIndexVal[0])
        myIndex.append(myIndexVal[0][0])
        
#Split the image
imgBlank = np.zeros_like(img)
imageArray = ([img, imgGray, imgBlur, imgCanny],
              [imgContours, imgBiggestContours, imgBlank, imgBlank])

imgStack = utis.stackImages(imageArray, 0.5) 

cv2.imshow("ImageStack", imgStack)
cv2.waitKey(0)
