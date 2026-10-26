import cv2


class CameraCapture:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    def __enter__(self):
        if not self.cap.isOpened():
            raise ValueError("Unable to open camera")
        return self.cap

    def __exit__(self, exc_type, exc_value, traceback):
        self.cap.release()