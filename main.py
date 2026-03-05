import sys

from pathlib import Path
from video_processor import VideoProcessor


def process_video_interactive():
    """Interactive mode to process video."""
    print("=" * 60)
    print("VIDEO PROCESSOR - Embed Logo & Subtitles")
    print("=" * 60)
    print()

    # Get input from user
    video_path = input("Enter path to video file: ").strip()
    subtitles_path = input("Enter path to subtitle file (.srt): ").strip()
    logo_path = input("Enter path to logo file (image): ").strip()
    output_path = input("Enter output path (press Enter for auto-generated): ").strip()

    output_path = output_path if output_path else None

    # Optional settings
    print("\n--- Optional Settings ---")
    logo_position = (
        input("Logo position (top-left/top-right/bottom-left/bottom-right) [top-left]: ").strip()
        or "top-left"
    )
    logo_scale = float(
        input("Logo scale (0.0-1.0, relative to video width) [0.2]: ").strip() or "0.2"
    )

    subtitle_position = input("Subtitle position (top/bottom) [bottom]: ").strip() or "bottom"
    fontsize = int(input("Subtitle font size [20]: ").strip() or "20")

    print("\n" + "=" * 60)
    print("Processing video...")
    print("=" * 60 + "\n")

    try:
        # Create processor and process video
        processor = VideoProcessor(video_path, output_path or "")
        processor.load_video()
        processor.add_logo(
            logo_path,
            position=logo_position,
            scale=logo_scale,
        )
        processor.add_subtitles(
            subtitles_path,
            fontsize=fontsize,
            position=subtitle_position,
        )
        output = processor.process()
        processor.cleanup()

        print(f"\n✓ Processing complete!")
        print(f"Output saved to: {output}")

    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)


def process_video_programmatic(
    video_path: str,
    subtitles_path: str,
    logo_path: str,
    output_path: str | None = None,
    logo_position: str = "top-left",
    logo_scale: float = 0.2,
):
    """
    Process video programmatically.

    Example usage:
        process_video_programmatic(
            video_path="input.mp4",
            subtitles_path="subtitles.srt",
            logo_path="logo.png",
            output_path="output.mp4"
        )
    """
    processor = VideoProcessor(video_path, output_path or "")
    processor.load_video()
    processor.add_logo(logo_path, position=logo_position, scale=logo_scale)
    processor.add_subtitles(subtitles_path)
    output = processor.process()
    processor.cleanup()
    return output


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line arguments provided
        if len(sys.argv) < 4:
            print("Usage: python main.py <video> <subtitles.srt> <logo>")
            sys.exit(1)

        video = sys.argv[1]
        subtitles = sys.argv[2]
        logo = sys.argv[3]
        output = sys.argv[4] if len(sys.argv) > 4 else None

        process_video_programmatic(video, subtitles, logo, output)
    else:
        # Interactive mode
        process_video_interactive()
