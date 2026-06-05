import os
import sys
import subprocess
from itertools import cycle
import os
from player.player import play
from player.yt import resolve_urls
import atexit

SESSION = "lofiplayer"


def run_player(video_source):
    print("\033[2J")

    if video_source.startswith("http"):
        playlist = cycle(resolve_urls(video_source))

        for url in playlist:
            sys.stdout.write("\tLoading, Please Wait...\n")
            sys.stdout.flush()

            state = play(url)

            if state == "QUIT":
                kill_tmux()
    else:
        state = play(video_source)

        if state == "QUIT":
            kill_tmux()


def launch_tmux(video_source):
    kill_tmux()

    subprocess.run(
        ["tmux", "new-session", "-d", "-s", SESSION, "-n", "video"],
        check=True,
    )

    subprocess.run(
        ["tmux", "set-option", "-g", "status", "off"],
        check=True,
    )

    subprocess.run(
        ["tmux", "new-window", "-t", SESSION, "-n", "lowfi", "lowfi"],
        check=True,
    )

    script = os.path.abspath(__file__)

    video_cmd = (
        f"{sys.executable} '{script}' '{video_source}'"
    )

    subprocess.run(
        [
            "tmux",
            "send-keys",
            "-t",
            f"{SESSION}:video",
            video_cmd,
            "C-m",
        ],
        check=True,
    )

    subprocess.run(
        ["tmux", "select-window", "-t", f"{SESSION}:video"],
        check=True,
    )

    subprocess.run(
        ["tmux", "attach-session", "-t", SESSION],
        check=True,
    )

def kill_tmux():
    subprocess.run(
        ["tmux", "kill-session", "-t", SESSION],
        stderr=subprocess.DEVNULL,
    )


atexit.register(kill_tmux)

def launcher(argument):
    if "TMUX" in os.environ:
        run_player(argument)
    else:
        launch_tmux(argument)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # print("Usage: python main.py <video-or-playlist-url>")
        # sys.exit(1)
        launcher("https://www.youtube.com/watch?v=-FlxM_0S2lA")  
    else:
        launcher(sys.argv[1])
