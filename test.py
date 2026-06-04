import cv2
import sys
import time
import shutil
import shutil
import numpy as np

cols, rows = shutil.get_terminal_size()
# ASCII = " .:-=+*#%@" # best ascii so far
ASCII = np.array(list(
    " .,:irsXA253hMHGS#9B&@"
))
# ASCII = np.array(list(" ▏▎▍▌▋▊▉█")) # better
# ASCII = np.array(list(ASCII))
# ASCII = " .'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
def get_terminal_size():
    return shutil.get_terminal_size((80, 24))

def get_render_size(frame, term_cols, term_rows):
    h, w, _ = frame.shape

    # character aspect ratio correction
    char_aspect = 0.55  

    # max width based on terminal
    max_width = term_cols

    # compute corresponding height
    height = int((h / w) * max_width * char_aspect)

    # if too tall → shrink width
    if height > term_rows:
        max_width = int(term_rows / ((h / w) * char_aspect))
        height = term_rows

    return max_width, height

# def frame_to_ascii(frame, width):
#     h, w = frame.shape
#     aspect_ratio = h / w
#     height = int(aspect_ratio * width * 0.5)

#     resized = cv2.resize(frame, (width, height))

#     return "\n".join(
#         "".join(ASCII[int(pixel) * len(ASCII) // 256] for pixel in row)
#         for row in resized
#     )

def frame_to_ascii_color_fast(frame, width):
    h, w, _ = frame.shape
    height = int((h / w) * width * 0.5)

    resized = cv2.resize(frame, (width, height))

    # --- vectorized brightness ---
    gray = (
        0.2126 * resized[:,:,2] +
        0.7152 * resized[:,:,1] +
        0.0722 * resized[:,:,0]
    ).astype(np.uint8)

    indices = (gray.astype(np.int32) * (len(ASCII)-1)) // 255
    chars = ASCII[indices]

    # --- build output (row-wise, not pixel-wise loops) ---
    lines = []
    for y in range(height):
        row_chars = chars[y]
        row_colors = resized[y]

        # build line in ONE join
        line = "".join(
            f"\x1b[38;2;{r};{g};{b}m{c}"
            for (b, g, r), c in zip(row_colors, row_chars)
        )
        lines.append(line)

    return "\n".join(lines) + "\x1b[0m"

def frame_to_ascii_fast(frame, width):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    h, w = gray.shape
    aspect_ratio = h / w
    height = int(aspect_ratio * width * 0.55)

    resized = cv2.resize(gray, (width, height))

    # vectorized mapping
    indices = (resized.astype(np.int32) * (len(ASCII)-1)) // 255
    chars = ASCII[indices]

    # join rows
    return "\n".join("".join(row) for row in chars)

def frame_to_ascii_color(frame, width):

    h, w, _ = frame.shape
    aspect_ratio = h / w
    height = int(aspect_ratio * width * 0.5)

    resized = cv2.resize(frame, (width, height))

    ascii_frame = []

    for row in resized:
        line = ""
        for b, g, r in row:
            # brightness for ASCII char
            gray = int((0.2126*r + 0.7152*g + 0.0722*b))
            char = ASCII[gray * (len(ASCII) - 1) // 255]

            # ANSI color (truecolor)
            line += f"\x1b[38;2;{r};{g};{b}m{char}"

        ascii_frame.append(line)

    return "\n".join(ascii_frame) + "\x1b[0m"

import time

def play_smooth(video_path):
    import cv2

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 24  # fallback
    if fps > 30:
        fps = 30  # cap to avoid too high CPU usage
        
    frame_duration = 1.0 / fps
    start_time = time.time()
    frame_count = 0

    print("\033[2J\033[?25l", end="")  # clear + hide cursor

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # --- render ---
        # ascii_frame = frame_to_ascii_color(frame, 100)

        term_cols, term_rows = shutil.get_terminal_size()

        width, height = get_render_size(frame, term_cols, term_rows - 1)

        ascii_frame = frame_to_ascii_color(frame, width)
        print("\033[H", end="")
        print(ascii_frame)

        # --- timing ---
        frame_count += 1
        expected_time = start_time + frame_count * frame_duration
        now = time.time()
        sleep_time = expected_time - now

        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            # we're behind → skip sleep (catch up)
            pass

    print("\033[?25h", end="")  # restore cursor
    cap.release()

# def play(video_path):
#     cap = cv2.VideoCapture(video_path)

#     fps = cap.get(cv2.CAP_PROP_FPS) or 24
#     delay = 1 / fps

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         term_width = get_terminal_size().columns

#         ascii_frame = frame_to_ascii_color(frame, term_width)

#         print("\033[H", end="")  # move cursor to top
#         print(ascii_frame)

#         time.sleep(delay)

#     cap.release()

def play(video_path):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 24

    TARGET_FPS = 20

    frame_duration = 1.0 / TARGET_FPS
    start_time = time.time()

    print("\033[2J\033[?25l", end="")  # clear + hide cursor

    frame_index = 0

    while True:
        now = time.time()
        expected_frame = int((now - start_time) / frame_duration)

        # # 🔑 Skip frames if we're behind
        # while frame_index < expected_frame:
        #     if not cap.grab():
        #         break
        #     frame_index += 1
        MAX_SKIP = 2

        skips = 0
        while frame_index < expected_frame and skips < MAX_SKIP:
            if not cap.grab():
                break
            frame_index += 1
            skips += 1

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