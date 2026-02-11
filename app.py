"""CLI entry point for generating a complete YouTube Shorts video."""

from __future__ import annotations

import argparse
from pathlib import Path

from generator import generate_short_content
from video_builder import build_short_video


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for topic, paths, and render settings."""
    parser = argparse.ArgumentParser(
        description="Generate YouTube Shorts scripts + captions + rendered video."
    )
    parser.add_argument("--topic", required=True, help="Psychology/facts topic")
    parser.add_argument(
        "--background",
        required=True,
        type=Path,
        help="Path to background video (example: assets/background.mp4)",
    )
    parser.add_argument(
        "--ffmpeg",
        required=True,
        type=Path,
        help="Absolute path to ffmpeg executable (example: C:/ffmpeg/bin/ffmpeg.exe)",
    )
    parser.add_argument(
        "--font-path",
        type=Path,
        default=Path("C:/Windows/Fonts/arial.ttf"),
        help="Font file path (Windows example: C:/Windows/Fonts/arial.ttf)",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="OpenAI model to use for hooks and script generation",
    )
    parser.add_argument("--duration", type=int, default=30, help="Output video duration")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("short.mp4"),
        help="Rendered output file path",
    )
    parser.add_argument(
        "--ass-output",
        type=Path,
        default=Path("captions.ass"),
        help="ASS subtitle output file path",
    )
    return parser.parse_args()


def main() -> None:
    """Run full generation pipeline and render short.mp4 with burned captions."""
    args = parse_args()

    # 1) Generate hooks/script/captions and persist ASS subtitles.
    generated = generate_short_content(
        topic=args.topic,
        ass_output_path=args.ass_output,
        model=args.model,
    )

    print("\nGenerated Hooks:")
    for idx, hook in enumerate(generated["hooks"], start=1):
        print(f"{idx}. {hook}")

    print("\nSelected Hook:")
    print(generated["selected_hook"])

    print("\nScript:")
    print(generated["script"])

    # 2) Build final vertical video with burned subtitle captions.
    output_path = build_short_video(
        ffmpeg_path=args.ffmpeg,
        background_video_path=args.background,
        ass_subtitle_path=Path(generated["ass_path"]),
        output_path=args.output,
        font_path=args.font_path,
        duration_seconds=args.duration,
    )

    print(f"\nVideo created: {output_path}")


if __name__ == "__main__":
    main()
