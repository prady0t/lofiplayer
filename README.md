# lofiplayer

ASCII-art video player for tmux with YouTube support.

## Features

- Plays videos in terminal using ASCII rendering
- Supports streaming from YouTube via `yt-dlp`
- Uses `tmux` sessions for video and low-fi controls

## Installation

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

## Testing

```bash
python -m pytest
```

## Development

This project uses a `src/` layout. The package source is under `src/lofiplayer`.

## License

MIT
