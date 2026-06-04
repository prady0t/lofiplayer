import cv2
import numpy as np

# ASCII = " .:-=+*#%@" # best ascii so far
ASCII = np.array(list(
    " .,:irsXA253hMHGS#9B&@"
))
# ASCII = np.array(list(" ▏▎▍▌▋▊▉█")) # better
# ASCII = np.array(list(ASCII))
# ASCII = " .'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

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

# def frame_to_ascii_fast(frame, width):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     h, w = gray.shape
#     aspect_ratio = h / w
#     height = int(aspect_ratio * width * 0.55)

#     resized = cv2.resize(gray, (width, height))

#     # vectorized mapping
#     indices = (resized.astype(np.int32) * (len(ASCII)-1)) // 255
#     chars = ASCII[indices]

#     # join rows
#     return "\n".join("".join(row) for row in chars)

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