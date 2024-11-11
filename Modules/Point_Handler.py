import itertools
import copy
import csv

class Point_Processing:
    
    def __init__(self):
        pass

    def make_landmark_list(self,image, landmarks):
        width, height = image.shape[1], image.shape[0]
        landmark_point = []

        for _, landmark in enumerate(landmarks.landmark):
            landmark_X = min(int(landmark.x * width), width - 1)
            landmark_Y = min(int(landmark.y * height), height - 1)
            landmark_point.append([landmark_X, landmark_Y])

        return landmark_point
    
    def normalize_Landmarks(self, landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)
        base_x, base_y = temp_landmark_list[0][0], temp_landmark_list[0][1]

        for index, landmark_point in enumerate(temp_landmark_list):
            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

        temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))

        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return (n / max_value)

        return list(map(normalize_, temp_landmark_list))   
    
    def logging_csv(self,number, landmark_list):

        if  (0 <= number <= 9):
            csv_path = 'Model/keypoint.csv'
            with open(csv_path, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *landmark_list])