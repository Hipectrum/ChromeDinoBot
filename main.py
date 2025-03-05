import pyautogui
import pydirectinput
from mss import mss
import numpy as np
import time
import subprocess
import keyboard

game_region = {"top": 120, "left": 650, "width": 600, "height": 200}

subprocess.run(["start", "chrome"], shell=True)

time.sleep(1)

pyautogui.hotkey('win', 'up')
pyautogui.hotkey('ctrl', '0')

time.sleep(0.5)

pyautogui.write('chrome://dino', interval=0.1)
pyautogui.press('enter')

time.sleep(1)

def jump():
    pyautogui.press("space")

def stop():
    return keyboard.is_pressed("f")

def restart():
    return pyautogui.press("space")

def duck():
    pydirectinput.keyDown("down")
    time.sleep(0.3)
    pydirectinput.keyUp("down")

jump()


with mss() as sct:
    while True:
        screenshot = sct.grab(game_region)
        img = np.array(screenshot)


        obstacle_pixels = img[120, 55:110]
        detected = np.any(
            (obstacle_pixels[:, 0] >= 168) & (obstacle_pixels[:, 0] <= 174) &
            (obstacle_pixels[:, 1] >= 168) & (obstacle_pixels[:, 1] <= 174) &
            (obstacle_pixels[:, 2] >= 168) & (obstacle_pixels[:, 2] <= 174)
        )

        obstacle_root = img[130, 55:110]
        root_pixels = np.any(
            (obstacle_root[:, 0] >= 168) & (obstacle_root[:, 0] <= 174) &
            (obstacle_root[:, 1] >= 168) & (obstacle_root[:, 1] <= 174) &
            (obstacle_root[:, 2] >= 168) & (obstacle_root[:, 2] <= 174)
        )

        vulture_pixels = img[95, 55:110]
        vulture_detected = np.any(
            (vulture_pixels[:, 0] >= 168) & (vulture_pixels[:, 0] <= 174) &
            (vulture_pixels[:, 1] >= 168) & (vulture_pixels[:, 1] <= 174) &
            (vulture_pixels[:, 2] >= 168) & (vulture_pixels[:, 2] <= 174)

        )

        clear_pixels = img[130, 55:110]
        path_clear = np.any(
            ((clear_pixels[:, 0] < 168) | (clear_pixels[:, 0] > 220)) &
            ((clear_pixels[:, 1] < 168) | (clear_pixels[:, 1] > 220)) &
            ((clear_pixels[:, 2] < 168) | (clear_pixels[:, 2] > 220))
        )

        game_over = img[60, 395:400]
        restart_game = np.any(
            (game_over[:, 0] >= 170) & (game_over[:, 0] <= 174) &
            (game_over[:, 1] >= 170) & (game_over[:, 1] <= 174) &
            (game_over[:, 2] >= 170) & (game_over[:, 2] <= 174)
        )

        if detected and root_pixels:
            print("Obstacle detected!")
            jump()

        elif vulture_detected and path_clear:
            print("Vulture detected!")
            duck()

        elif restart_game:
            print("Game restarting.")
            restart()

        if stop():
            print("Game stopped.")
            break

print('Game started. Press "f" for stop.')

