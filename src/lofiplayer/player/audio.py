import subprocess

SESSION = "lofiplayer"
# VIDEO_URL = "https://youtu.be/CFGLoQIhmow?si=DD79iVNM37Q4yulB"
VIDEO_URL =  "https://www.youtube.com/watch?v=iWkB6pI6opI&list=PLv1quoEqqgjAihdJtJZVKWtZWo_vD2y6U&index=1"

# Kill old session if present
subprocess.run(
    ["tmux", "kill-session", "-t", SESSION],
    stderr=subprocess.DEVNULL,
)

# Create session
subprocess.run(
    ["tmux", "new-session", "-d", "-s", SESSION, "-n", "video"],
    check=True,
)

subprocess.run(
    ["tmux", "set-option", "-g", "status", "off"],
    check=True,
)

# # Hidden lowfi window
subprocess.run(
    ["tmux", "new-window", "-t", SESSION, "-n", "lowfi", "lowfi"],
    check=True,
)

# Video window:
# Run player, then kill entire tmux session when it exits.
video_cmd = (
    f"python ../main.py '{VIDEO_URL}'; "
    f"tmux kill-session -t {SESSION}"
)

subprocess.run(
    ["tmux", "send-keys",
     "-t", f"{SESSION}:video",
     video_cmd,
     "C-m"],
    check=True,
)

# Show video window
subprocess.run(
    ["tmux", "select-window", "-t", f"{SESSION}:video"],
    check=True,
)

# User enters tmux
subprocess.run(
    ["tmux", "attach-session", "-t", SESSION],
)

# When the video exits, the session is killed,
# attach-session returns, and the user is back
# at their original terminal prompt.