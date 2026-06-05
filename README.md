# lofiplayer

ASCII-art video player for tmux with YouTube support.

## Features

- Plays videos in terminal using ASCII rendering
- Supports streaming from YouTube via `yt-dlp`
- Uses `tmux` sessions for video and low-fi controls

## Requirements

- `python` 3.10+
- `tmux`
- `lowfi` (installed separately, e.g. via Cargo)

## Installation

Make sure [lowfi](https://github.com/talwat/lowfi) and tmux are already installed first.
```bash
python -m pip install .
```

For editable development installs:

```bash
python -m pip install -e .[dev]
```

## Usage

```bash
python -m lofiplayer "https://www.youtube.com/watch?v=-FlxM_0S2lA"
```

If no URL is provided, a default YouTube video is launched.

| Key | Function |
|-----|----------|
| `s` | Skip Song |
| `Space` | Play/Pause audio and video |
| `q`, `CTRL+C` | Quit |
| `n` | next video |

## Gallery

<img width="1680" height="841" alt="Screenshot 2026-06-06 at 2 13 34 AM" src="https://github.com/user-attachments/assets/17f2009a-769a-42f8-9bf2-b8b962a589de" />


<img width="1680" height="849" alt="Screenshot 2026-06-06 at 2 11 39 AM" src="https://github.com/user-attachments/assets/0a202e19-f489-4d29-84b0-a36fbc7b8f38" />


<img width="1680" height="878" alt="Screenshot 2026-06-06 at 2 10 31 AM" src="https://github.com/user-attachments/assets/e9282eec-e7fd-461d-9956-745878d5e90a" />


<img width="1680" height="841" alt="Screenshot 2026-06-06 at 2 16 21 AM" src="https://github.com/user-attachments/assets/09900137-7402-4c81-98ac-5c7e8e597bb4" />





## License

MIT
