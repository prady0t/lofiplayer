
import shutil


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