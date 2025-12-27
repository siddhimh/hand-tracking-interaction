import cv2
import mediapipe as mp 

class HandTracker:
    
    def __init__(self):
        self.cap =cv2.VideoCapture(0)
        self.mpHands= mp.solutions.hands
        
        self.hands= self.mpHands.Hands(       
            static_image_mode= False,
            max_num_hands =2,
            min_detection_confidence= 0.6,
            max_detection_confidence= 0.6
        )
        
    
    def get_frame(self):
        img = self.cap.read()
        imgRGB= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        results= self.hands.process(imgRGB)
        print(results.multi_hand_landmarks)
        
        return results
        