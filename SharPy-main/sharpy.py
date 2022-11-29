# Importing all the necessary packages

import numpy as np
import cv2 as cv
from collections import deque
import mediapipe as mp
from math import hypot

# Import ends here


# Creating utils for mediapipe
mp_drawing = mp.solutions.drawing_utils #drawing
mp_drawing_styles = mp.solutions.drawing_styles #drawing
mp_hands = mp.solutions.hands #track hand


# Function to detect and track Index finger and Middle finger.


def CreateMarks(image):
    isDrawing = False
    x_2, y_2 = 0, 0 #index
    z_1, z_2 = 0, 0 #thumb
#write trigger
    with mp_hands.Hands(
        model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

        image.flags.writeable = False
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = hands.process(image)
#writing from here
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        landmarkList = [] #18 hand marks present in hand..
#if handd is in front of camera then below will run
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for _id, landm in enumerate(hand_landmarks.landmark):
                    h, w, c = image.shape
                    x, y = int(landm.x * w), int(landm.y * h) #coordinate if finger in frame
                    landmarkList.append([_id, x, y])

        if landmarkList != []:
            x_1, y_1 = landmarkList[12][1], landmarkList[12][2] #index
            x_2, y_2 = landmarkList[8][1], landmarkList[8][2] #middle finger
            z_1, z_2 = landmarkList[4][1], landmarkList[4][2] #thumb
            cv.circle(image, (x_1, y_1), 6, (255, 255, 255), cv.FILLED) #making circle
            cv.circle(image, (x_2, y_2), 6, (255, 255, 255), cv.FILLED) #marking circle

            distance = hypot(x_2 - x_1, y_2 - y_1) #coor distance betwwn them trhough func of index and middle
            if distance >= 0 and distance < 35: # will not work if index and middle finger dist in this
                isDrawing = False
            else:
                isDrawing = True #it will work

    return image, isDrawing, [x_2, y_2] , [z_1, z_2]


# Driver function starts from here
def open():
    cap = cv.VideoCapture(0)
    h = int(cap.get(3))
    w = int(cap.get(4))
    print(h, w)

    img = cv.imread("./window_layout_bg.png", 1)
    resize_img = cv.resize(img, (640, 480))
    img2gray = cv.cvtColor(resize_img, cv.COLOR_BGR2GRAY)
    ret, mask = cv.threshold(img2gray, 1, 255, cv.THRESH_BINARY)
# to render the drawing everytime
    bpoints = [deque(maxlen=1024)]
    gpoints = [deque(maxlen=1024)] #index meh green color ka point rhega 
    rpoints = [deque(maxlen=1024)]
    ypoints = [deque(maxlen=1024)]

    blue_index = 0
    green_index = 0
    red_index = 0
    yellow_index = 0

    colorIndex = 0

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
    canvas = None
    shape = "line"

    while True:

        xp, yp = 0, 0
        ret, frame = cap.read(0)
        eraserMode = False

        frame = cv.flip(frame, 1) #laptop camera ulta img dekhta hai so 1 mtlb flip horizontally
        if canvas is None:
            canvas = np.zeros_like(frame)
        frame, isDrawing, center, thumb = CreateMarks(frame)

        roi = frame[-0 - 0 : h, -w - w : h] 
        roi[np.where(mask)] = 0
        roi += resize_img #image is inserted in roi which in shown in webcam

        if isDrawing:
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center) #data pushed in queue and display
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)

        else:
            if center[1] <= 50: #upr k nav bar se y coor check hoga
                if 53 <= center[0] <= 85:         #selection of different color  if x is within color
                    colorIndex = 0  # For Blue
                if 133 <= center[0] <= 168:
                    colorIndex = 3  # For Yellow
                if 218 <= center[0] <= 253:
                    colorIndex = 1  # For green
                if 300 <= center[0] <= 333:
                    colorIndex = 2  # For red

                if 476 <= center[0] <= 512: #screen clear
                    bpoints = [deque(maxlen=512)] #creating new queue so that previous queue is destroyed and frame is clear
                    gpoints = [deque(maxlen=512)]
                    ypoints = [deque(maxlen=512)]
                    rpoints = [deque(maxlen=512)]

                    blue_index = 0
                    red_index = 0 # queue is again to start
                    green_index = 0
                    yellow_index = 0

            if center[0] >= 587: #x coor to right bar
                if 64 <= center[1] <= 102: # y bar coor then select triangle
                    shape = "triangle"  # triangle
                if 134 <= center[1] <= 165:
                    shape = "circle"  # circle
                if 215 <= center[1] <= 251:
                    shape = "square"  # square
                if 294 <= center[1] <= 332:
                    shape = "line"  # square

            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512)) #shape drawing
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1

        points = [bpoints, gpoints, rpoints, ypoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])): #2d queue to access all point in queue
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue #frame k bahar to draw nhi  wrna draw
                    if shape == "line":

                        cv.line(
                            frame, points[i][j][k - 1], points[i][j][k], colors[i], 7 #i to select color and 7 is thickness
                        )
                    elif shape == "square" and isDrawing:
                        cv.rectangle(frame, center, thumb, colors[i], 7)

                    elif shape == "circle" and isDrawing:
                        result = int(
                            (
                                (
                                    ((thumb[0] - center[0]) ** 2)
                                    + ((thumb[1] - center[1]) ** 2)
                                )
                                ** 0.5
                            )
                        )
                        if result < 0:
                            result = -1 * result
                        cv.circle(frame, center, result, colors[i], 7)

        cv.imshow("SharPy", frame)

        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


