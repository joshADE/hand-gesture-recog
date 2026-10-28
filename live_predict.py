import cv2
import numpy as np
import mediapipe as mp
import joblib

from camera_capture import CameraCapture
from key_manager import KeyBindingImpl, KeyManager
from key_manager import KeyManager
from opencv_drawer import OpenCVDrawer
from opencv_keyboard import OpenCVKeyBoardInput
from mediapipe_landmarker import MediaPipeLandmarker

# Load the trained machine learning model (scikit-learn)
print("Loading prediction model...")
model = joblib.load('gesture_model.pkl')

# Setup MediaPipe Hand Landmarker
media_pipe_landmarker = MediaPipeLandmarker('hand_landmarker.task')

def quit_program():
    cv2.destroyAllWindows()
    exit()

# Keyboard management for quitting the program
openCVKeyboard = OpenCVKeyBoardInput()
keyManager = KeyManager(openCVKeyboard)
keyManager.register_key_binding(KeyBindingImpl('q', lambda event: quit_program()))

# for drawing on the OpenCV window
drawer = OpenCVDrawer()

# Open Webcam
with CameraCapture(0) as cap:
    print("Live Predictor Active! Press 'q' to quit.")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?) ...")
            continue

        # Flip frame horizontally to mirror the view
        frame = cv2.flip(frame, 1)
        
        # Convert frame for MediaPipe
        mp_image = media_pipe_landmarker.create_srgb_image(data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        detection_result = media_pipe_landmarker.detect_landmarks(mp_image)

        current_gesture = "No Gesture Detected"

        if detection_result.hand_landmarks:
            for hand_landmarks in detection_result.hand_landmarks:
                # Put the 63 coordinates into a list

                landmarks = []
                for lm in hand_landmarks:
                    landmarks.extend([lm.x, lm.y, lm.z])

                # Convert to a 2D NumPy array (scikit-learn expects 2D shape)
                input_data = np.array([landmarks])

                # Make a prediction
                current_gesture = model.predict(input_data)[0]

                # Draw the landmarks on the frame
                drawer.draw_landmarks(frame, hand_landmarks)

        # Display the predicted gesture
        drawer.draw_gesture_label(frame, current_gesture, (10, 30))

        cv2.imshow("Live Gesture Recognition", frame)

        # Press 'q' to exit
        if keyManager._keyboard_input.is_key_pressed('q'):
            break

cv2.destroyAllWindows()