import time
from typing import Tuple

import numpy as np
from PIL import ImageGrab, ImageOps
import pyautogui


class GameCoordinates:
    """
    Class to store the coordinates of important game elements.
    """
    def __init__(self):
        self.replay_button = (1279, 777)
        self.dinosaur_top_right = (178, 828)

    @property
    def detection_box(self) -> Tuple[int, int, int, int]:
        """
        Calculate the bounding box for detecting obstacles.

        Returns:
            Tuple[int, int, int, int]: The coordinates of the bounding box (left, top, right, bottom).
        """
        left = self.dinosaur_top_right[0] + 230
        top = self.dinosaur_top_right[1] + 98
        right = self.dinosaur_top_right[0] + 330
        bottom = self.dinosaur_top_right[1] + 100
        return left, top, right, bottom


def restart_game(coords: GameCoordinates) -> None:
    """
    Restart the game by clicking the replay button and setting the initial game state.

    Args:
        coords (GameCoordinates): The coordinates of important game elements.
    """
    pyautogui.click(coords.replay_button)
    time.sleep(0.1)
    pyautogui.keyDown('down')


def jump() -> None:
    """
    Perform the jump action by releasing the down key, pressing the space key, and then pressing the down key again.
    """
    pyautogui.keyUp('down')
    pyautogui.keyDown('space')
    time.sleep(0.1)
    pyautogui.keyUp('space')
    pyautogui.keyDown('down')


def image_grab(coords: GameCoordinates, level: int) -> int:
    """
    Capture the game screen within the dinosaur's bounding box and calculate the sum of grayscale pixel values.

    Args:
        coords (GameCoordinates): The coordinates of important game elements.
        level (int): The current level of the game.

    Returns:
        int: The sum of grayscale pixel values within the dinosaur's bounding box.
    """
    box = coords.detection_box
    left, top, right, bottom = box[0] + level, box[1], box[2] + level, box[3]
    image = ImageGrab.grab(bbox=(left, top, right, bottom))
    gray_image = ImageOps.grayscale(image)
    pixel_values = np.array(gray_image.getcolors())
    pixel_sum = pixel_values.sum()
    print(f"Pixel sum: {pixel_sum}")
    return pixel_sum


def main() -> None:
    """
    Main game loop.
    """
    coords = GameCoordinates()
    restart_game(coords)
    level = 0
    target_pixel_sum = 455  # Adjust this value based on your game environment

    while True:
        pixel_sum = image_grab(coords, level)
        if pixel_sum != target_pixel_sum:
            jump()
            level += 8
            time.sleep(0.1)


if __name__ == "__main__":
    main()
