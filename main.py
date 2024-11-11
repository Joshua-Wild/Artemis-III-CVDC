import cv2
import csv
import mediapipe as mp
import time
import threading


from Model.Keypoint_classifier import KeyPointClassifier
from Modules.Point_Handler import Point_Processing
from Modules.Drone_Handler import Drone_module
from Modules.UI import *


def handle_keypress():
    key = cv2.waitKey(10)
    

    number = -1

    if key == 27:  # ESC to quit
        global running
        running = False
        exit
    
    if 48 <= key <= 57:  # 0 ~ 9
        number = key - 48
    if key == 116:  # t
         global Training
         Training =  not Training
    
    return number

def side(processed_landmark_list, classifier, drone):

    hand_sign_id = classifier(processed_landmark_list)
    if not Training:
        drone.control_drone_with_gesture(hand_sign_id)

def main():
    drone = Drone_module()
    classifier = KeyPointClassifier()
    Point_Processor  = Point_Processing()
    webcam = VideoStream(width=640, height=480, fps=30).start()

    global current_time, dt, running, Training
    running = True
    Training = False

    # MediaPipe hands setup
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    processing_interval = 0.1  # Process gestures every 100ms
    last_processed_time = 0

    
    while running:
        img = webcam.read()
       
        number = handle_keypress()
    
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        #Overlay.draw_info(img)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmark_list = Point_Processor.make_landmark_list(img, hand_landmarks)
                processed_landmark_list = Point_Processor.normalize_Landmarks(landmark_list)
                brect = Overlay.make_bounding_rect(img, hand_landmarks)
                
                # draw the landmarks and bounding box
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                Overlay.draw_bounding_rect(img, brect, Training)
                
                if Training:
                    Point_Processor.logging_csv(number, processed_landmark_list)
                
                current_time = time.time()
                dt = current_time - last_processed_time
                if not Training and dt > processing_interval:
                    last_processed_time = current_time
                    threading.Thread(target=side, args=(processed_landmark_list, classifier, drone)).start()
                    
      
        cv2.imshow('Drone Control', img)

        if cv2.waitKey(1) == ord('q'):
            drone.disconnect(10)
            break

    webcam.stop()
    cv2.destroyAllWindows()


# Read labels ###########################################################
with open('Model/keypoint_classifier_label.csv',
            encoding='utf-8-sig') as f:
    keypoint_classifier_labels = csv.reader(f)
    keypoint_classifier_labels = [
        row[0] for row in keypoint_classifier_labels
        ]

# Run the main function
if __name__ == '__main__':
    main()
''''
TO DO
- impliment emergency landing and forced landing procedure when escaoe is pressed
- Make BEAUTIFUL

'''

