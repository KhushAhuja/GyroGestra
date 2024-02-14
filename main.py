import mediapipe as mp
import cv2
from pyfirmata import Arduino, util, SERVO
from time import sleep

port = 'COM4'
pin = 10
board = Arduino(port)

board.digital[pin].mode = SERVO

def rotateservo(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.015)

mp_drawings = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

video = cv2.VideoCapture(0)

rotate_clockwise = False
rotate_anticlockwise = False

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
    while video.isOpened():
        _, frame = video.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        imageHeight, imageWidth, _ = image.shape
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for handLandmarks in results.multi_hand_landmarks:
                mp_drawings.draw_landmarks(image, handLandmarks, mp_hands.HAND_CONNECTIONS)

                hand_landmarks = [landmark for landmark in handLandmarks.landmark]

                
                if hand_landmarks[mp_hands.HandLandmark.WRIST].x < hand_landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x:
                    
                    rotate_clockwise = False
                    rotate_anticlockwise = True
                else:
                
                    rotate_anticlockwise = False
                    rotate_clockwise = True

        if rotate_clockwise:
            rotateservo(pin, 10)
        elif rotate_anticlockwise:
            rotateservo(pin, 170)

        cv2.imshow('Hand Tracking', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

video.release()
