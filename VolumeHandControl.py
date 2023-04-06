import cv2
import mediapipe as mp
import time
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480 # Width and Hight of the camera -> If I set as 1240, 960, the image of the camera gets wider
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
cTime = 0

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()
# print(volume.GetVolumeRange())
# < (-65.25, 0.0, 0.03125) > 0 is the max and -65 the minimun

minVol = volumeRange[0]
maxVol = volumeRange[1]

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    lmList = []
    handNo = 0

    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
            #cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)

    if len(lmList) != 0:
        #print(lmList)
        # print(lmList[4], lmList[8]) # The tip of the fingers that are gonna change the volume
        # Let's change that for variables
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2 # getting the center of the line

        cv2.circle(img, (x1, y1), 8, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 8, (0, 255, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 3)

        length = math.hypot(x2-x1, y2-y1) # To get the length of the line
        # Hand range: 20 - 200 --> this lenght will be used to increase or low the volume
        # ( 20 is my tumbs close together and 200 when they are splitted)
        # Volume range: -65 - 0

        # We need to convert this two ranges, for that we will use numpy
        vol = np.interp(length, [20, 200], [minVol, maxVol]) # first the lenght, than the conversions ranges
        volBar = np.interp(length, [20, 200], [400, 150])
        volPer = np.interp(length, [20, 200], [0, 100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)


        if length < 20 or length > 200:

            cv2.circle(img, (x1, y1), 8, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 8, (255, 0, 0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'Volume: {str(int(volPer))} %', (100, 400), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {str(int(fps))}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("image", img)
    cv2.waitKey(1)
