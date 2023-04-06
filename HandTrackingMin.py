import cv2
import mediapipe as mp
import time

# Inicializing the web can (The '0' is because I only have 1 webcan.
cap = cv2.VideoCapture(0)
# This is kind of a formallity in order to use this module
mpHands = mp.solutions.hands
hands = mpHands.Hands()
# To draw the 21 points
mpDraw = mp.solutions.drawing_utils

# To evaluate the performance over time:
pTime = 0 # previous time
cTime = 0 # currente time

"""
The Hands() function parameters explained: This function operates detecting and tracking.
  def __init__(self,
               static_image_mode=False, -> Basically, if it is set True, it takes more time.
               max_num_hands=2,
               model_complexity=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5): -> If this parameter is below 0.5, it will try to detect again.
"""
"""
# Basic code to run our webcan
while True:
    success, img = cap.read()

    cv2.imshow("image", img)
    cv2.waitKey(1)
"""
"""
while True:
    success, img = cap.read()
    # Converting the image type
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Processing the converted image
    results = hands.process(imgRGB)
    #print(results) -> <class 'mediapipe.python.solution_base.SolutionOutputs'> So far, if we bring our hand to the camera, nothing really changes.
    # We need to check if the model will be able to find a hand or even multiple hands

    cv2.imshow("image", img)
    cv2.waitKey(1)
"""
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    print(results.multi_hand_landmarks)
    """
    When I put my hand:
    landmark {
  x: 0.7633700370788574
  y: 0.7889255285263062
  z: -0.08569016307592392
}
]
When there is no hand:
None
    """

    # To extract the information of each possible hand:
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # To actually get this information: the id number and the landmarks (x, y) coordinates:
            for id, lm in enumerate(handLms.landmark): # The id number is the index number of the landmark
                #print(id, lm)
                """
                That's id 0 with the coordinates of the landmark
                0 x: 0.5885829925537109
                y: 0.44216060638427734
                z: 9.23457399437666e-09
                
                We will use the x and y to find the location of the hand. 
                But the location should be in pixels (500 pixels in width and 250 pixels in high) and the output
                is in decimals that are actually a ratio of the image. We need to multiply it with the width and high 
                to get the pixel value:
                """
                h, w, c = img.shape # gives us the high, width and channel of the image
                cx, cy = int(lm.x*w), int(lm.y*h) # gives us the coordinates of x and y of the landmatks in pixels
                print(id, cx, cy)
                # [4, 8, 12, 16, 20] -> list with all finger points
                """
                The id correspondes of a landmark (0 - 21) and the x,y are the coordinates of that landmark at that
                period of time. It keeps updating.
                """
                if id == 4 or id == 8 or id == 12 or id == 16 or id == 20:
                    # Here I am drawing a circle in every finger point
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)






            # To show the landmarks and the connections
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    # To display in the image the time: we can observe that the project is very responsive
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("image", img)
    cv2.waitKey(1)