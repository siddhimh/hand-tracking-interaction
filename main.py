import cv2

# Open the default camera
cam = cv2.VideoCapture(0)

# Get the default frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

while True:
    ret, frame = cam.read()

    # Write the frame to the output file
    out.write(frame)

    # Display the captured frame
    cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cam.release()
out.release()
cv2.destroyAllWindows()



import cv2
import mediapipe as mp
import math

def distance(point1, point2):
    return math.hypot(point2.x - point1.x, point2.y - point1.y)

def is_pinch(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    return distance(thumb_tip, index_tip) < 0.05

def is_open_hand(hand_landmarks):
    tips = [8, 12, 16, 20]  # fingers
    base = [5, 9, 13, 17]
    for t, b in zip(tips, base):
        if distance(hand_landmarks.landmark[t], hand_landmarks.landmark[b]) < 0.1:
            return False
    return True

mp_hands= mp.solutions.hands
mp_drawings= mp.solutions.drawing_utils
objects = [{"pos": (300,200), "radius": 30}]


hands= mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7    
    )

cap=cv2.VideoCapture(0)

while True: 
    ret, frame = cap.read()
    if not ret:
        break
    
    frame= cv2.flip(frame,1)
    rgb_frame= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    result= hands.process(rgb_frame)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawings.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
            height, width, _ = frame.shape
            x = int(hand_landmarks.landmark[8].x * width)
            y = int(hand_landmarks.landmark[8].y * height)
            for obj in objects:
               obj_x, obj_y = obj["pos"]
               if math.hypot(x - obj_x, y - obj_y) < obj["radius"]:
                   obj_color = (0,255,0)  # hover
               else:
                   obj_color = (0,0,255)
               cv2.circle(frame, obj["pos"], obj["radius"], obj_color, -1)

            if is_pinch(hand_landmarks):
                 for obj in objects:
                   if math.hypot(x - obj["pos"][0], y - obj["pos"][1]) < obj["radius"]:
                     obj["pos"] = (x, y)
                 cv2.putText(frame, "Pinch", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            elif is_open_hand(hand_landmarks):
                cv2.putText(frame, "Open", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
   
    cv2.imshow("Hand tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
    

cap.realse()
cv2.destroyAllWindows()   
