import cv2
from .core.handtrack import HandTracker

cap = cv2.VideoCapture(0)
tracker = HandTracker()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    tracker.process(frame)
    tracker.draw(frame)

    cv2.imshow("XR Hand Input", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
