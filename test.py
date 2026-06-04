import cv2
import sys
import time
import shutil
import shutil
import numpy as np
from lofiplayer.ascii_converter import frame_to_ascii_color_fast
from lofiplayer.controls import Controls
import tty
import termios
import curses


def play(video_path):
    PLAY = True
    PAUSE = False
    QUIT = False
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 24

    TARGET_FPS = 20

    frame_duration = 1.0 / TARGET_FPS
    start_time = time.time()

    print("\033[2J\033[?25l", end="")  # clear + hide cursor
    frame_index = 0
    with Controls() as controls:
        while not QUIT:
            key = controls.get_key()
            if key == "QUIT":
                QUIT = True
            now = time.time()
            expected_frame = int((now - start_time) / frame_duration)

            MAX_SKIP = 2

            skips = 0
            while frame_index < expected_frame and skips < MAX_SKIP:
                if not cap.grab():
                    break
                frame_index += 1
                skips += 1
            if key == "SPACE":
                PLAY = not PLAY
                PAUSE = not PAUSE
            if PAUSE:
                time.sleep(0.1)
                start_time += time.time() - now  # adjust start time to account for pause
                continue
            ret, frame = cap.read()
            if not ret:
                break

            frame_index += 1

            # --- dynamic size ---
            term_cols, term_rows = shutil.get_terminal_size()
            width = term_cols

            # --- render ---
            # ascii_frame = frame_to_ascii_color(frame, width)
            ascii_frame = frame_to_ascii_color_fast(frame, width)

            print("\033[H", end="")
            print(ascii_frame)

            # tiny sleep to avoid maxing CPU
            time.sleep(0.001)
    print("\033[?25h", end="")  # restore cursor
    cap.release()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test.py <video>")
    else:
        print("\033[2J")  # clear once
        play(sys.argv[1])