import cv2

import mediapipe as mp
import time
import threading

from Model.Keypoint_classifier import KeyPointClassifier
from Modules.Point_Handler import Point_Processing
from Modules.Drone_Control import DroneController
from constants import processing_interval
from Modules.UI import *


def handle_keypress(key, Training):
    
    number = -1
   

    if 48 <= key <= 57:  # 0 ~ 9
        number = key - 48

    elif key == 116:  # t
         
         Training =  not Training

    return number, Training

def side(processed_landmark_list, classifier, drone, Training):

    hand_sign_id = classifier(processed_landmark_list)

    if not Training:
        drone.control_drone_with_gesture(hand_sign_id)
    

def main():

    

    # Initialize drone
    drone_controller = DroneController()
    drone_active = drone_controller.initialize()

    Video = VideoStream(width=640, height=480, fps=30).start()
    
    classifier = KeyPointClassifier()
    Point_Processor  = Point_Processing()


    # MediaPipe hands setup
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

 
    Training = True

    last_processed_time = 0
                    
    while True:
        img = Video.read()

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        key = cv2.waitKey(10)
        if key == 27:  # ESC to quit
            Video.stop()
            break
           
        
        number, Training = handle_keypress(key, Training)

        Overlay.draw_info(img)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                
                #Generate landmark list and process landmarks
                landmark_list = Point_Processor.make_landmark_list(img, hand_landmarks)
                processed_landmark_list = Point_Processor.normalize_Landmarks(landmark_list)
                brect = Overlay.make_bounding_rect(img, hand_landmarks)
                
                # draw the landmarks and bounding box
                
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                Overlay.draw_bounding_rect(img, brect, Training)
                
                # log landmarksn if training mode is active
                if Training: Point_Processor.logging_csv(number, processed_landmark_list)
                

                current_time = time.time()
                dt = current_time - last_processed_time
                if not Training and dt > processing_interval:
                    last_processed_time = current_time
                    threading.Thread(target=side, args=(processed_landmark_list, classifier, drone_controller, Training)).start()
                    
      
        cv2.imshow('Drone Control', img)

        
    #clean up
    if drone_active: drone_controller.disconnect()
    Video.stop()
    cv2.destroyAllWindows()


# Run the main function
if __name__ == '__main__':
    main()
''''
TO DO
- impliment emergency landing and forced landing procedure when escaoe is pressed
- Make BEAUTIFUL

'''

