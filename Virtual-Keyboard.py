"""import libraries :
        cv2:for take picture and  edit on it
        medipipe:for detect hands
        time:for make delay on typing (fix DDDDDDD----> D)
        cvzone:for draw buttons
        pynput:for type in windows
"""
import cv2
import mediapipe as mp
import time
import numpy as np
import cvzone
from pynput.keyboard import Controller

# Webcam setup
webcam = cv2.VideoCapture(0)#teke picture from webcam
webcam.set(3, 1280)         # Webcam resolution
webcam.set(4, 720)          # Webcam resolution

# Hand tracking setup
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

# Keyboard setup
keyboard = Controller()

# Keyboard buttons setup
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

# Initialize the final text string
finalText = ""

# Button class to define button properties
class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

# Create button instances for each key
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

# Main loop
while True:
    # Read frame from webcam
    _ , image = webcam.read()
    image = cv2.flip(image, 1)  # Mirror the video

    # Process the image to detect hands
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])
                if id == 8:
                    cv2.circle(image, center=(x, y), radius=8, color=(0, 255, 0))
                    x1 = x
                    y1 = y
                if id == 12:
                    cv2.circle(image, center=(x, y), radius=8, color=(255, 0, 250))
                    x2 = x
                    y2 = y
        dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) // 4    #calculate distance between index and middle finger
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 5)
        print(f"{dist}____{x2}_____{y2}")                       #print distance and x and y of middle finger

        # Check if (x2, y2) is inside a button and dist is less than 7
        for i, button in enumerate(buttonList):
            if (button.pos[0] - 50 <= x2 <= button.pos[0] + 50 and
                button.pos[1] - 50 <= y2 <= button.pos[1] + 50 and
                dist < 7):
                keyboard.press(button.text) #write character in windows
                time.sleep(0.15)

    # Draw buttons on the image
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(image, (x, y, w, h), 20, rt=0)
        cv2.rectangle(image, button.pos, (x + w, y + h), (200, 0, 0), cv2.FILLED)
        cv2.putText(image, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    # Show the virtual keyboard(app window)
    cv2.imshow("Virtual Keyboard", image)

    # Exit the program if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam
webcam.release()
cv2.destroyAllWindows()
