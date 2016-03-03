#!/usr/bin/python
import cv2
import numpy as np

# img = cv2.imread('leena.jpeg')
img = cv2.imread(sys.argv[1])
blur = cv2.GaussianBlur(img,(7,7),0)
cv2.imwrite(sys.argv[1],blur)

# return blur
# cv2.imshow('Blur',blur)
# cv2.waitKey(0)
# cv2.destroyAllWindows()        # Closes displayed windows
