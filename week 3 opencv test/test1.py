import cv2

color = cv2.imread("test.png",1)
gray = cv2.imread("test.png", 0)
unchanged = cv2.imread("test.png", -1)
cv2.imshow("color", color)
cv2.imshow("gray", gray)
cv2.imshow("unchanged", unchanged)
cv2.waitKey(0)
