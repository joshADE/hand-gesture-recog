import cv2
import numpy as np
import mediapipe as mp
import joblib

from camera_capture import CameraCapture
from mediapipe_landmarker import MeadiaPipeLandmarker

# 1. Load the trained machine learning model (scikit-learn)
print("Loading trained gesture model...")
model = joblib.load('gesture_model.pkl')

# 2. Setup MediaPipe Hand Landmarker
media_pipe_landmarker = MeadiaPipeLandmarker('hand_landmarker.task')

# 3. Open Webcam
with CameraCapture(0) as cap:
    print("Live Predictor Active! Press 'q' to quit.")
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip horizontally for a mirror view
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Convert frame for MediaPipe
        mp_image = media_pipe_landmarker.create_srgb_image(data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        detection_result = media_pipe_landmarker.detect_landmarks(mp_image)

        current_gesture = "No Hand Detected"

        if detection_result.hand_landmarks:
            for hand_landmarks in detection_result.hand_landmarks:
                # Extract the 63 coordinates
                landmark_list = []
                for lm in hand_landmarks:
                    landmark_list.extend([lm.x, lm.y, lm.z])

                # Convert to a 2D NumPy array (scikit-learn expects 2D shape: [1, 63])
                input_data = np.array([landmark_list])

                # Make a prediction using the trained MLP model
                current_gesture = model.predict(input_data)[0]

                # Draw green circles on the hand joints
                for lm in hand_landmarks:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # Display the predicted gesture on the screen
        cv2.putText(frame, f"Gesture: {current_gesture}", (30, 50), 
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 3)

        cv2.imshow("Live Gesture Recognition", frame)

        # Press 'q' to exit
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()