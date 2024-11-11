import cv2
import numpy as np
import threading



class Overlay:
    def __init__(self):
        pass

    def make_bounding_rect(image, landmarks):
        webcam_width, webcam_height = image.shape[1], image.shape[0]
        landmark_array = np.empty((0, 2), int)

        for _, landmark in enumerate(landmarks.landmark):
            landmark_X = min(int(landmark.x * webcam_width), webcam_width - 1)
            landmark_Y = min(int(landmark.y * webcam_height), webcam_height - 1)
            landmark_point = [np.array((landmark_X, landmark_Y))]
            landmark_array = np.append(landmark_array, landmark_point, axis=0)

        x, y, w, h = cv2.boundingRect(landmark_array)
        return [x, y, x + w, y + h]

    def draw_bounding_rect(image, brect, Training):
        if brect:
            if Training:
                cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]), (0, 255, 0), 1)
            else:
                cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]), (255, 0, 0), 1)


    #def draw_info(image):
        # Using cv2.putText()
        
            #cv2.putText(image, "MODE", (300, 10),cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale = 1.0, color = (255, 255, 255), thickness = 1)
            #cv2.rectangle()


# Threaded Video Capture class to ensure non-blocking camera input
class VideoStream:
    def __init__(self, src=0, width=320, height=240, fps=30):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.stream.set(cv2.CAP_PROP_FPS, fps)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        threading.Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.stream.release()