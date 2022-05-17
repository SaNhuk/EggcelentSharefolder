import cv2
import imutils
from transform import four_point_transform
import numpy as np


kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
img_path = 'test10.jpg'
big_img = cv2.imread(img_path)
rot_img = cv2.rotate(big_img, cv2.ROTATE_180)
big_img = rot_img
cv2.imshow('org img', big_img)
cv2.waitKey(0)

ratio = big_img.shape[0] / 500
org = big_img.copy()
img = imutils.resize(big_img, height=500)
cv2.imshow('resizing', img)
cv2.waitKey(0)

gray_img = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
edged_img = cv2.Canny(blur_img, 75, 200)
cv2.imshow('edged', edged_img)
cv2.waitKey(0)

cnts, _ = cv2.findContours(edged_img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        doc = approx
        break

p = []
for d in doc:
    tuple_point = tuple(d[0])
    cv2.circle(img, tuple_point, 3, (0, 0, 255), 4)
    p.append(tuple_point)
cv2.imshow('Corner points detected', img)
cv2.waitKey(0)

warped = four_point_transform(org, doc.reshape(4, 2) * ratio)
sharpened = cv2.filter2D(warped, -1, kernel)
warped = sharpened
cv2.imshow("Warped", imutils.resize(warped, height=1000))
cv2.waitKey(0)



