"""Caption chunking and ASS subtitle generation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class CaptionChunk:
    """Represents one timed caption line."""

    text: str
    start: float
    end: float


def chunk_script(script: str, min_words: int = 3, max_words: int = 6) -> List[CaptionChunk]:
    """Split a script into caption lines with ~1s timing per line.

    The chunk size is constrained to 3-6 words and line durations are kept within
    0.8-1.2 seconds.
    """
    words = script.split()
    chunks: List[CaptionChunk] = []

    i = 0
    t = 0.0

    # Walk through words and create chunks between min_words and max_words.
    while i < len(words):
        remaining = len(words) - i

        # Prefer 4 words for readability while honoring remaining words.
        size = 4
        if remaining <= max_words:
            size = max(min_words, remaining)
        else:
            size = max(min_words, min(max_words, size))

        text = " ".join(words[i : i + size])

        # Keep each caption within required 0.8s-1.2s window.
        duration = 1.0
        start = t
        end = t + duration

        chunks.append(CaptionChunk(text=text, start=start, end=end))

        i += size
        t = end

    return chunks


def _ass_time(seconds: float) -> str:
    """Convert seconds to ASS H:MM:SS.cc format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int(round((seconds - int(seconds)) * 100))
    return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"


def build_ass_subtitles(captions: List[CaptionChunk], font_name: str = "Arial") -> str:
    """Generate a full ASS subtitle document from caption chunks."""
    header = f"""[Script Info]
Title: Auto-generated Shorts Captions
ScriptType: v4.00+
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font_name},68,&H00FFFFFF,&H000000FF,&H00111111,&H64000000,0,0,0,0,100,100,0,0,1,4,0,2,60,60,220,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    events = []

    # Build one Dialogue row per caption chunk.
    for caption in captions:
        line = (
            f"Dialogue: 0,{_ass_time(caption.start)},{_ass_time(caption.end)},"
            f"Default,,0,0,0,,{caption.text}"
        )
        events.append(line)

    return header + "\n".join(events) + "\n"


def write_ass_file(content: str, output_path: Path) -> Path:
    """Write ASS subtitle content to disk and return the file path."""
    output_path.write_text(content, encoding="utf-8")
    return output_path
