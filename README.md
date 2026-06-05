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

## Testing

```bash
python -m pytest
```

## Development

This project uses a `src/` layout. The package source is under `src/lofiplayer`.

## License

MIT
