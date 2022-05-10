from cv2 import TonemapReinhard
import numpy as np
import cv2 as cv
import sys
import time

# <-- Constants -->
minWorkpieceArea = 100 
workpieceEdge = 205   # a
containerEdge = 490   # b
leftMargin = 15       # c
topMargin = 15        # d
tolerance = 0.05

# <-- Regions       | Colors -->
#       1.............Red
#       2.............Green
#       3.............Yellow
#       4.............Blue

# <-- Read image and convert it to HSV -->
def readImage(imgPath):
    bgr = cv.imread(imgPath, cv.IMREAD_COLOR)
    if bgr is None:
        sys.exit("Not found input file")
    hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
    return bgr, hsv

# <-- Extract mask of the desired colors -->
def inRange(hsv):
    th1 = cv.bitwise_or(
        cv.inRange(hsv, (170, 70, 70), (180, 255, 255)),
        cv.inRange(hsv, (0, 70, 70), (10, 255, 255))
    )
    th2 = cv.inRange(hsv, (50, 70, 70), (70, 255, 255))
    th3 = cv.inRange(hsv, (25, 70, 70), (33, 255, 255))
    th4 = cv.inRange(hsv, (120, 70, 70), (130, 255, 255))
    th = (th1, th2, th3, th4)
    for t in th:
        kernel = np.ones((3,3), np.uint8)
        t = cv.erode (t, kernel=kernel)
        t = cv.dilate(t, kernel=kernel) 
    return th

# <-- Check the condition of having 4 colors -->
def checkFirstCond(th):
    for thresh in th:
        contours = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[0]
        res = 0
        for con in contours:
            # print(cv.contourArea(con))
            if cv.contourArea(con) >= minWorkpieceArea:
                res += 1
        if res != 1:
            return False
    return True

def between(x, a, b):
    return (a <= x) and (x <= b) 

# <-- If condition 1 is matched, check the condition of color order -->
def checkSecondCond(th):
    #<-- Alias for edges -->
    a = workpieceEdge
    b = containerEdge
    c = leftMargin
    d = topMargin

    
    desiredX = (c + a // 2,         \
                b - c - a // 2,     \
                c + a // 2,         \
                b - c - a // 2      ) 
    desiredY = (d + a // 2,         \
                d + a // 2,         \
                b - d - a // 2,     \
                b - d - a // 2      )
    # print(desiredX)
    # print(desiredY)
    for i, thresh in enumerate(th):
        M = cv.moments(thresh)
        if M['m00'] != 0:
            cX = int(M['m10']/M['m00'])
            cY = int(M['m01']/M['m00'])
            # print(f"cX = {cX} \ncY = {cY}\n")
            if not between(cX, desiredX[i] - a*tolerance, desiredX[i] + a*tolerance) \
            or not between(cY, desiredY[i] - a*tolerance, desiredY[i] + a*tolerance):
                return False
    return True

def resultGen(th):
    c1 = checkFirstCond(th)
    if c1:
        c2 = checkSecondCond(th)
        if c2:
            print("Đủ 4 màu, đúng thứ tự")
        else:
            print("Đủ 4 màu nhưng không đúng thứ tự")
        return c2
    else:
        print("Không đủ 4 màu")
        return False

# <-- Main -->
if __name__ == "__main__":
    # print(f"Arguments count: {len(sys.argv)}")
    # for i, arg in enumerate(sys.argv):
    #     print(f"Argument {i:>6}: {arg}")
    start_time = time.time()
    img, hsv = readImage("./assets/phoi4.png")
    th = inRange(hsv)
    # for t in th:
    #     cv.imshow("t", t)
    #     cv.waitKey(0)

    print(resultGen(th))
    print(f"Thời gian chạy: {time.time() - start_time} giây")