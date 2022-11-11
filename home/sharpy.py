import numpy as np
import cv2 as cv
from .createmarks import *
from collections import deque


def open_cv():
        cap = cv.VideoCapture(0)
        h = int(cap.get(3))
        w = int(cap.get(4))
        print(h, w)


        img = cv.imread("./window_layout_bg.png", 1)
        resize_img = cv.resize(img, (640, 480))
        img2gray = cv.cvtColor(resize_img, cv.COLOR_BGR2GRAY)
        ret, mask = cv.threshold(img2gray, 1, 255, cv.THRESH_BINARY)

        bpoints = [deque(maxlen=1024)]
        gpoints = [deque(maxlen=1024)]
        rpoints = [deque(maxlen=1024)]
        ypoints = [deque(maxlen=1024)]


        blue_index = 0
        green_index = 0
        red_index = 0
        yellow_index = 0


        colorIndex = 0

        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
        canvas = None


        while True:

            xp, yp = 0, 0
            ret, frame = cap.read(0)
            eraserMode = False

            frame = cv.flip(frame, 1)
            if canvas is None:
                canvas = np.zeros_like(frame)
            frame, isDrawing, center, thumb = createmarks.CreateMarks(frame)

            roi = frame[-0 - 0 : h, -w - w : h]
            roi[np.where(mask)] = 0
            roi += resize_img

            if isDrawing:
                if colorIndex == 0:
                    bpoints[blue_index].appendleft(center)
                elif colorIndex == 1:
                    gpoints[green_index].appendleft(center)
                elif colorIndex == 2:
                    rpoints[red_index].appendleft(center)
                elif colorIndex == 3:
                    ypoints[yellow_index].appendleft(center)

            else:
                if center[1] <= 50:
                    if 53 <= center[0] <= 85:
                        colorIndex = 0  # For Blue
                    if 133 <= center[0] <= 168:
                        colorIndex = 3  # For Yellow
                    if 218 <= center[0] <= 253:
                        colorIndex = 1  # For green
                    if 300 <= center[0] <= 333:
                        colorIndex = 2  # For red

                    if 476 <= center[0] <= 512:
                        bpoints = [deque(maxlen=512)]
                        gpoints = [deque(maxlen=512)]
                        ypoints = [deque(maxlen=512)]
                        rpoints = [deque(maxlen=512)]

                        blue_index = 0
                        red_index = 0
                        green_index = 0
                        yellow_index = 0

                bpoints.append(deque(maxlen=512))
                blue_index += 1
                gpoints.append(deque(maxlen=512))
                green_index += 1
                rpoints.append(deque(maxlen=512))
                red_index += 1
                ypoints.append(deque(maxlen=512))
                yellow_index += 1

            points = [bpoints, gpoints, rpoints, ypoints]
            for i in range(len(points)):
                for j in range(len(points[i])):
                    for k in range(1, len(points[i][j])):
                        if points[i][j][k - 1] is None or points[i][j][k] is None:
                            continue
                        cv.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 5)

            cv.imshow("SharPy", frame)

            if cv.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv.destroyAllWindows()
