# YouTube Shorts Auto-Generator (Python Mini-Framework)

This project auto-generates YouTube Shorts content using OpenAI models and assembles a vertical video with burned captions via FFmpeg.

## Modules

- `hooks.py` — generates multiple short hook lines for psychology/facts topics.
- `scripts.py` — turns a hook into a ~45–65 word script for a 20–30 second short.
- `captions.py` — chunks the script into timed caption lines and exports ASS subtitles.
- `video_builder.py` — renders a vertical 1080x1920 video with looped/tiled background and burned captions.
- `generator.py` — orchestrates hook → script → captions.
- `app.py` — CLI entry point that prints content and renders `short.mp4`.

## Requirements

- Python 3.9+
- FFmpeg installed
- OpenAI API key in environment (`OPENAI_API_KEY`)

Install Python dependency:

```bash
pip install openai
```

## FFmpeg install and verification

### Windows
1. Download FFmpeg static build from: https://ffmpeg.org/download.html
2. Extract (example path): `C:/ffmpeg`
3. Verify:

```bash
C:/ffmpeg/bin/ffmpeg.exe -version
```

### macOS (Homebrew)
```bash
brew install ffmpeg
ffmpeg -version
```

### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install -y ffmpeg
ffmpeg -version
```

## Example usage

Example background path:

- `assets/background.mp4`

Run generation + render:

```bash
python app.py \
  --topic "why your brain loves unfinished tasks" \
  --background assets/background.mp4 \
  --ffmpeg C:/ffmpeg/bin/ffmpeg.exe \
  --font-path C:/Windows/Fonts/arial.ttf \
  --output short.mp4
```

Result:

- prints generated hooks + selected hook + script
- writes `captions.ass`
- creates `short.mp4`
