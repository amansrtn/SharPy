import numpy as np
import cv2 as cv
import mediapipe as mp
from math import hypot


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def CreateMarks(image):
    isDrawing = False
    x_2, y_2 = 0, 0
    z_1, z_2 = 0, 0

    with mp_hands.Hands(
        model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as hands:

        image.flags.writeable = False
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = hands.process(image)

        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        landmarkList = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for _id, landm in enumerate(hand_landmarks.landmark):
                    h, w, c = image.shape
                    x, y = int(landm.x * w), int(landm.y * h)
                    landmarkList.append([_id, x, y])

        if landmarkList != []:
            x_1, y_1 = landmarkList[12][1], landmarkList[12][2]
            x_2, y_2 = landmarkList[8][1], landmarkList[8][2]
            z_1, z_2 = landmarkList[4][1], landmarkList[4][2]
            cv.circle(image, (x_1, y_1), 6, (255, 255, 255), cv.FILLED)
            cv.circle(image, (x_2, y_2), 6, (255, 255, 255), cv.FILLED)
            distance = hypot(x_2 - x_1, y_2 - y_1)
            if distance >= 0 and distance < 35:
                isDrawing = False
            else:
                isDrawing = True

    return image, isDrawing, [x_2, y_2], [z_1, z_2]
