#!/usr/bin/python
import cv2
import numpy as np
import sys

# img = cv2.imread('lenna.jpg')
img = cv2.imread(sys.argv[1])
blur = cv2.blur(img,(15,15))
cv2.imwrite(sys.argv[2],blur)
# return blur
# cv2.imshow('Blur',blur)
# cv2.waitKey(0)
# cv2.destroyAllWindows()        # Closes displayed windows
