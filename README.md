# Video Marker

A Python-based video processor that embeds subtitles (SRT format) and logos into videos with an easy-to-use interface.

## Quick Start

### 1. Prerequisites

- Python 3.7+
- FFmpeg installed on your system

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Processor

**Interactive Mode:**

```bash
python main.py
```

**With Command Line Arguments:**

```bash
python main.py input.mp4 subtitles.srt logo.png output.mp4
```

**Programmatic (in your code):**

```python
from video_processor import VideoProcessor

processor = VideoProcessor("input.mp4")
processor.load_video()
processor.add_logo("logo.png")
processor.add_subtitles("subtitles.srt")
output = processor.process()
processor.cleanup()
```

## Usage Details

For comprehensive usage instructions, see [USAGE.md](USAGE.md).

### Logo Positioning

- `top-left`, `top-right`, `bottom-left`, `bottom-right`

### Supported Formats

- **Video**: MP4, AVI, MOV, MKV (any FFmpeg-supported format)
- **Subtitles**: SRT format only
- **Images**: PNG, JPG, GIF (any PIL-supported format)

## Installation

### macOS

```bash
brew install ffmpeg
pip install -r requirements.txt
```

### Ubuntu/Debian

```bash
sudo apt-get install ffmpeg
pip install -r requirements.txt
```

### Windows

1. Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Add FFmpeg to your PATH
3. Run: `pip install -r requirements.txt`

## Example

```bash
# Process a video with subtitles and logo
python main.py movie.mp4 subtitles.srt logo.png final_video.mp4
```

## License

MIT License - Feel free to use in your projects!
