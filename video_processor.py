import os
import pysrt

from pathlib import Path
from typing import Optional, Tuple
from PIL import Image

# Compatibility fix for Pillow 11.0+ with moviepy
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS  # type: ignore

from moviepy.editor import (
    VideoFileClip,
    ImageClip,
    TextClip,
    CompositeVideoClip,
)


class VideoProcessor:
    """Process video by embedding subtitles and logo."""

    def __init__(self, video_path: str, output_path: Optional[str] = None):
        """
        Initialize the video processor.

        Args:
            video_path: Path to the input video file
            output_path: Path for the output file (optional, auto-generated if not provided)
        """
        self.video_path = video_path
        self.output_path = output_path or self._generate_output_path(video_path)
        self.video = None

    @staticmethod
    def _generate_output_path(video_path: str) -> str:
        """Generate output path based on input path."""
        base_path = Path(video_path)
        return str(base_path.parent / f"{base_path.stem}_processed.mp4")

    def load_video(self):
        """Load the video file."""
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Video file not found: {self.video_path}")
        self.video = VideoFileClip(self.video_path)
        return self

    def add_logo(
        self,
        logo_path: str,
        position: str = "top-left",
        scale: float = 0.2,
    ) -> "VideoProcessor":
        """
        Add logo to the video.

        Args:
            logo_path: Path to the logo image file
            position: Position of logo - 'top-left', 'top-right', 'bottom-left', 'bottom-right'
            scale: Scale of the logo relative to video width (0.0-1.0)

        Returns:
            Self for method chaining
        """
        if self.video is None:
            raise RuntimeError("Video not loaded. Call load_video() first.")
        if not os.path.exists(logo_path):
            raise FileNotFoundError(f"Logo file not found: {logo_path}")

        # Validate logo format
        try:
            Image.open(logo_path)
        except Exception as e:
            raise ValueError(f"Invalid image file: {logo_path}. Error: {e}")

        logo_clip = ImageClip(logo_path)

        # Calculate logo size based on video width
        video_width = self.video.w
        logo_width = int(video_width * scale)
        logo_clip = logo_clip.resize(width=logo_width)  # type: ignore

        # Calculate position
        x, y = self._calculate_position(position, logo_clip)

        # Add logo for the entire video duration
        logo_clip = logo_clip.set_duration(self.video.duration).set_position((x, y))

        # Composite the logo with the video
        self.video = CompositeVideoClip([self.video, logo_clip])

        return self

    def add_subtitles(
        self,
        subtitles_path: str,
        fontsize: int = 20,
        font: str = "DejaVu-Sans",
        color: str = "white",
        position: str = "bottom",
    ) -> "VideoProcessor":
        """
        Add subtitles to the video from an SRT file.

        Args:
            subtitles_path: Path to the .srt subtitle file
            fontsize: Font size for subtitles
            font: Font family
            color: Text color (color name or hex)
            position: Position - 'top' or 'bottom'

        Returns:
            Self for method chaining
        """
        if self.video is None:
            raise RuntimeError("Video not loaded. Call load_video() first.")
        if not os.path.exists(subtitles_path):
            raise FileNotFoundError(f"Subtitle file not found: {subtitles_path}")

        # Load subtitles
        try:
            subs = pysrt.open(subtitles_path)
        except Exception as e:
            raise ValueError(f"Failed to load subtitle file: {e}")

        # Create text clips for each subtitle
        text_clips = []
        for sub in subs:
            start_time = self._timedelta_to_seconds(sub.start)
            end_time = self._timedelta_to_seconds(sub.end)

            text_clip = TextClip(
                sub.text,
                fontsize=fontsize,
                font=font,
                color=color,
                method="caption",
                size=(self.video.w - 40, None),
            )

            # Set duration and timing
            text_clip = text_clip.set_duration(end_time - start_time).set_start(
                start_time
            )

            # Position the subtitle
            if position == "top":
                text_clip = text_clip.set_position(("center", 20))
            else:  # bottom
                text_clip = text_clip.set_position(
                    ("center", self.video.h - text_clip.h - 20)
                )

            text_clips.append(text_clip)

        # Composite subtitles with video
        self.video = CompositeVideoClip([self.video] + text_clips)

        return self

    def process(self, codec: str = "libx264", audio_codec: str = "aac") -> str:
        """
        Process and save the video.

        Args:
            codec: Video codec to use
            audio_codec: Audio codec to use

        Returns:
            Path to the output file
        """
        if self.video is None:
            raise RuntimeError("Video not loaded. Call load_video() first.")

        print(f"Processing video: {self.video_path}")
        print(f"Output will be saved to: {self.output_path}")

        self.video.write_videofile(
            self.output_path,
            codec=codec,
            audio_codec=audio_codec,
            verbose=False,
            logger=None,
        )

        print(f"Video processed successfully: {self.output_path}")
        return self.output_path

    def cleanup(self):
        """Clean up resources."""
        if self.video is not None:
            self.video.close()

    @staticmethod
    def _timedelta_to_seconds(td) -> float:
        """Convert timedelta to seconds."""
        return td.hours * 3600 + td.minutes * 60 + td.seconds + td.milliseconds / 1000

    @staticmethod
    def _calculate_position(position: str, clip) -> Tuple[int, int]:
        """Calculate x, y position based on position string."""
        # This will be set relative to video later
        positions = {
            "top-left": ("left", "top"),
            "top-right": ("right", "top"),
            "bottom-left": ("left", "bottom"),
            "bottom-right": ("right", "bottom"),
        }

        if position not in positions:
            raise ValueError(
                f"Invalid position: {position}. Must be one of {list(positions.keys())}"
            )

        horiz, vert = positions[position]

        # For now, return string positions (will be resolved by moviepy)
        margin = 20
        x = margin if horiz == "left" else -margin
        y = margin if vert == "top" else -margin

        return (x, y)
