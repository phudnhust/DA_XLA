from dis import dis
import cv2 as cv
from matplotlib.pyplot import contour
import numpy as np
import sys
from ptHelper import mid2Point, dist2Point

def loadImage(imgPath):
    img = cv.imread(imgPath, cv.IMREAD_COLOR)
    if img is None:
        sys.exit('Not found input file')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    edge = cv.Canny(gray, 30, 200)
    cv.imshow("edge", edge)
    contours, hierarchy = cv.findContours(edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    # cv.drawContours(img, contours, -1, (0, 255, 0), 3)

    return img, contours
    pass


def procContours(img, contours):
    for c in contours:
        minAreaRect = cv.minAreaRect(c)
        centerPoint = minAreaRect[0]
        vList = cv.boxPoints(minAreaRect)
        # cv2.minAreaRect(points) -> (center(x, y), (width, height), angle of rotation)
        m1 = mid2Point(vList[0], vList[1])
        m2 = mid2Point(vList[1], vList[2])
        m3 = mid2Point(vList[2], vList[3])
        m4 = mid2Point(vList[3], vList[0])
        print(m1)
        if dist2Point(m1, m3) > dist2Point(m2, m4):
            # chiều dài gắp là (m2, m4)
            color = (0, 255, 0)
            thickness = 9
            img = cv.line(img, m2, m4, color, thickness)
        else:
            # chiều dài gắp là (m1, m3)
            color = (0, 255, 0)
            thickness = 9
            img = cv.line(img, m1, m3, color, thickness)
        print(vList)
    return img


if __name__ == '__main__':
    img, contours = loadImage('./demoWorkpiece.png')
    img = procContours(img, contours)
    cv.imshow('contours + chieu dai gap', img)
    cv.waitKey(0)