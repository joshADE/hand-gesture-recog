import cv2

from keyboard_input import KeyBoardInput


class OpenCVKeyBoardInput(KeyBoardInput):
    def get_key(self) -> str:
        key = cv2.waitKey(1) & 0xFF
        if key != 255:  # 255 means no key was pressed
            return chr(key)
        return None

    def is_key_pressed(self, key: str) -> bool:
        pressed_key = self.get_key()
        return pressed_key == key

    def read_key(self) -> str:
        return self.get_key()