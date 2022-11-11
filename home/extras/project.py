
import numpy as np
import cv2 as cv
import createmarks
cap=cv.VideoCapture(0)
h = int(cap.get(3))
w = int(cap.get(4))

#cord_blue = {'x': 

img = cv.imread('window_layout_bg.png', 1)
resize_img = cv.resize(img, (640,480))
img2gray = cv.cvtColor(resize_img, cv.COLOR_BGR2GRAY)
ret, mask = cv.threshold(img2gray, 1, 255, cv.THRESH_BINARY)

	
	
while True:
    ret, frame = cap.read(0)
    
    # frame = createmarks.CreateMarks(cap) 
    #Uncomment above line for creating lines on fingers.
    
    #Fliping the frame horizontally
    frame = cv.flip(frame,1)
    
    roi = frame[-0-0:h, -w-w:h]
    roi[np.where(mask)] = 0
    roi += resize_img
    #cv.namedWindow('SharPy', flags=cv.WINDOW_GUI_EXPANDED)
    cv.imshow('SharPy', frame)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
