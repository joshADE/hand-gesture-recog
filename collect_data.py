import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import csv
import os

from camera_capture import CameraCapture
from key_manager import KeyBindingImpl, KeyManager
from opencv_keyboard import OpenCVKeyBoardInput
from mediapipe_landmarker import MediaPipeLandmarker


# 1. Setup MediaPipe Hand Landmarker passing in the path to the hand_landmarker.task file
media_pipe_landmarker = MediaPipeLandmarker('hand_landmarker.task')

# 2. Setup CSV File for Data Collection
csv_file_path = 'gesture_dataset_1.csv'
file_exists = os.path.isfile(csv_file_path)

# Open the CSV file in append mode
f = open(csv_file_path, mode='a', newline='')
writer = csv.writer(f)

# The hand_landmarker.task model outputs 21 hand landmarks, each with x, y, z coordinates. Therefore, we have 63 features (21 * 3) plus 1 label column for the gesture name.
# If file is new, write the header of the csv file with 63 features (x,y,z for 21 points) + 1 label column
if not file_exists:
    header = []
    for i in range(21):
        header.extend([f'x_{i}', f'y_{i}', f'z_{i}'])
    header.append('label')
    writer.writerow(header)

print("Data Collector Active!")
key_to_label = {
    ord('1'): "Thumbs_Up",
    ord('2'): "Fist",
    ord('3'): "Peace",
    ord('q'): "Quit"
}
# print the key bindings for user reference
for key, label in key_to_label.items():
    print(f"Press '{chr(key)}' for {label}")

# the functionality to quit the program and save the dataset
def quit_program():
    f.close()
    cv2.destroyAllWindows()
    print(f"Dataset saved successfully to {csv_file_path}!")
    exit()

current_label = "None"

# the functionality to handle key presses and record the hand landmarks along with the corresponding label
def label_action(label):
    def handle_landmarks_and_record(event, data):
        print(data)
        global current_label
        current_label = label
        landmark_list = []
        hand_landmarks = data['hand_landmarks']
        for lm in hand_landmarks:
            landmark_list.extend([lm.x, lm.y, lm.z])
        landmark_list.append(current_label)
        writer.writerow(landmark_list)
        print(f"Recorded: {current_label}")
    return handle_landmarks_and_record

# setting up the key manager and registering key bindings for each gesture label
openCVKeyboard = OpenCVKeyBoardInput()
keyManager = KeyManager(openCVKeyboard)
keyManager.register_key_binding(KeyBindingImpl('1', lambda event, data: label_action("Thumbs_Up")(event, data)))
keyManager.register_key_binding(KeyBindingImpl('2', lambda event, data: label_action("Fist")(event, data)))
keyManager.register_key_binding(KeyBindingImpl('3', lambda event, data: label_action("Peace")(event, data)))
keyManager.register_key_binding(KeyBindingImpl('q', lambda event: quit_program()))



# 3. Open Webcam
with CameraCapture(0) as cap:
    print("Data Collector Active! Press 'q' to quit.")
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

        if detection_result.hand_landmarks:
            for hand_landmarks in detection_result.hand_landmarks:
                # Draw joints on screen
                for lm in hand_landmarks:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

                # Check for key presses to record data
                data = {'hand_landmarks': hand_landmarks}
                keyManager.handle_key_events(data)

        # Display active label on video feed
        cv2.putText(frame, f"Active Label: {current_label}", (10, 30), 
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        cv2.imshow("Data Collector", frame)

        if keyManager._keyboard_input.is_key_pressed('q'):
            break

cap.release()
f.close()
cv2.destroyAllWindows()