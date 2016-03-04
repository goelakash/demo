#!/usr/bin/python
import cv2
import sys

# img = cv2.imread('leena.jpeg')
img = cv2.imread(sys.argv[1])
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(sys.argv[2],gray_image)
# cv2.imshow('gray_image',gray_image)
# cv2.waitKey(0)                 # Waits forever for user to press any key
# cv2.destroyAllWindows()        # Closes displayed windows

#End of Code