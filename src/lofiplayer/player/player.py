import cv2
import sys
import time
from .ascii_converter import frame_to_ascii_color_fast
from .controls import Controls
from .window import get_terminal_size
import subprocess

SESSION = "lofiplayer"


def play(video_path):
    PLAY = True
    PAUSE = False
    state = "PLAYING"
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 24

    frame_duration = 1.0 / fps
    start_time = time.time()

    print("\033[2J\033[?25l", end="")  # clear + hide cursor
    frame_index = 0
    with Controls() as controls:
        while True:
            key = controls.get_key()
            if key == "QUIT":
                state = "QUIT"
                return state
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
                subprocess.run(
                    ["tmux", "send-keys", "-t", f"{SESSION}:lowfi", "p"],
                    stderr=subprocess.DEVNULL,
                ) 
            if PAUSE:
                time.sleep(0.1)
                start_time += time.time() - now  # adjust start time to account for pause
                continue
            if key == "SKIP":
                subprocess.run(
                    ["tmux", "send-keys", "-t", f"{SESSION}:lowfi", "s"],
                    stderr=subprocess.DEVNULL,
                )
            if key == "NEXT":
                break
            ret, frame = cap.read()
            if not ret:
                break

            frame_index += 1

            # --- dynamic size ---
            term_cols, term_rows = get_terminal_size()
            width = term_cols

            # --- render ---
            ascii_frame = frame_to_ascii_color_fast(frame, width)

            sys.stdout.write("\033[H")
            sys.stdout.write(ascii_frame)
            sys.stdout.flush()

            # tiny sleep to avoid maxing CPU
            next_frame_time = start_time + frame_index * frame_duration
            sleep_time = next_frame_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
    print("\033[?25h", end="")  # restore cursor
    cap.release()