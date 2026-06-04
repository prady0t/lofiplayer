import sys
import tty
import termios
import select


class Controls:
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setcbreak(self.fd)

    def get_key(self):
        dr, _, _ = select.select([sys.stdin], [], [], 0)

        if not dr:
            return None

        ch = sys.stdin.read(1)

        if ch == "q":
            return "QUIT"

        if ch == " ":
            return "SPACE"

        if ch == "\x1b":
            if sys.stdin.read(1) != "[":
                return None

            direction = sys.stdin.read(1)

            if direction == "D":
                return "LEFT"

            if direction == "C":
                return "RIGHT"

        return None

    def cleanup(self):
        termios.tcsetattr(
            self.fd,
            termios.TCSADRAIN,
            self.old_settings,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.cleanup()