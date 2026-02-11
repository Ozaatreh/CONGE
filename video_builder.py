"""FFmpeg video assembly for vertical YouTube Shorts with burned subtitles."""

from __future__ import annotations

import subprocess
from pathlib import Path


def build_short_video(
    ffmpeg_path: Path,
    background_video_path: Path,
    ass_subtitle_path: Path,
    output_path: Path,
    font_path: Path = Path("C:/Windows/Fonts/arial.ttf"),
    duration_seconds: int = 30,
) -> Path:
    """Create a 1080x1920 short by looping background and burning ASS subtitles.

    Args:
        ffmpeg_path: Absolute path to the ffmpeg executable.
        background_video_path: Source background clip path.
        ass_subtitle_path: ASS subtitle file path.
        output_path: Final MP4 path.
        font_path: Font path for subtitle rendering (Windows-safe default).
        duration_seconds: Output length in seconds.

    Returns:
        Path to rendered output video.
    """
    if not ffmpeg_path.is_absolute():
        raise ValueError("ffmpeg_path must be an absolute path.")

    # Escape paths for FFmpeg filter usage.
    ass_for_filter = str(ass_subtitle_path).replace("\\", "/").replace(":", "\\:")
    font_dir = str(font_path.parent).replace("\\", "/").replace(":", "\\:")

    # Filter pipeline:
    # 1) Split into 4 streams and tile as a 2x2 mosaic.
    # 2) Scale/crop to 1080x1920 vertical canvas.
    # 3) Burn ASS subtitles with explicit fontsdir.
    filter_complex = (
        "[0:v]split=4[v0][v1][v2][v3];"
        "[v0]scale=540:960[t0];"
        "[v1]scale=540:960[t1];"
        "[v2]scale=540:960[t2];"
        "[v3]scale=540:960[t3];"
        "[t0][t1][t2][t3]xstack=inputs=4:layout=0_0|540_0|0_960|540_960[tiled];"
        "[tiled]crop=1080:1920:0:0,"
        f"subtitles='{ass_for_filter}':fontsdir='{font_dir}'[v]"
    )

    cmd = [
        str(ffmpeg_path),
        "-y",
        "-stream_loop",
        "-1",
        "-i",
        str(background_video_path),
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-t",
        str(duration_seconds),
        "-r",
        "30",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        str(output_path),
    ]

    # Run FFmpeg process and raise if rendering fails.
    subprocess.run(cmd, check=True)
    return output_path
