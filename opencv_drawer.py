import cv2


class OpenCVDrawer:
    def __init__(self):
        pass

    def draw_landmarks(self, frame, hand_landmarks):
        # Draw landmarks on the frame
        for lm in hand_landmarks:
            x = int(lm.x * frame.shape[1])
            y = int(lm.y * frame.shape[0])
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    def draw_gesture_label(self, frame, gesture_label, position=(10, 30), font_scale=1, color=(255, 0, 0), thickness=2):
        # Draw the gesture label on the frame
        cv2.putText(frame, f'Gesture: {gesture_label}', position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
        