import cv2
import numpy as np
import sys

# Loading image, padding it and find contours
def loadExtractContour(imgPath):
    img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
    if img is None:
        sys.exit("Not found input image")

    # # Padding img
    # img_pad = np.zeros([img.shape[0] + 50, img.shape[1] + 50, 3])
    # img_pad += 100      # grey color BGR: [100, 100, 100] <=> hex: #646464
    # img_pad[20:, 20:, :] = img

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    ROI_number = 0
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    print(len(cnts))
    return img, cnts

def writeText(img, org, txt):
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    color = (255, 0, 0)
    thickness = 2
    img = cv2.putText(img, txt, org, font, fontScale, color, thickness, cv2.LINE_AA)

# This function does: draw contours, approx Polygons and write text to each contour
def procContour(img, cnts):
    for cnt in cnts:
        cv2.drawContours(img, [cnt.astype(int)], 0, (0,255,0), 3)

        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cX = int(M['m10']/M['m00'])
            cY = int(M['m01']/M['m00'])
        org = (cX, cY)

        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 5:
            writeText(img, org, "Pentagon")
        elif len(approx) == 3:
            writeText(img, org, "Triangle")
        elif len(approx) == 4:
            writeText(img, org, "Rectangle")
        elif len(approx) == 6:
            writeText(img, org, "Hexa")
        elif len(approx) == 8:
            writeText(img, org, "Octa")
        elif len(approx) > 12:
            writeText(img, org, "Circle")

if __name__ == '__main__':
    imgPath = 'assets/shapes.jpg'
    img, cnts = loadExtractContour(imgPath)
    cv2.imshow("img after padding", img)

    procContour(img, cnts)
    cv2.imshow("img with shapes", img)
    cv2.waitKey()

