#!/usr/bin/python
import cv2
import numpy as np
import sys

# img = cv2.imread('leena.jpeg')
img = cv2.imread(sys.argv[1])
blur = cv2.blur(img,(5,5))
return blur
# cv2.imshow('Blur',blur)
# cv2.waitKey(0)
# cv2.destroyAllWindows()        # Closes displayed windows
