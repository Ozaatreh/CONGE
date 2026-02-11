"""Pipeline orchestrator: hook -> script -> captions (ASS)."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from captions import CaptionChunk, build_ass_subtitles, chunk_script, write_ass_file
from hooks import generate_hooks
from scripts import generate_script


def generate_short_content(
    topic: str,
    ass_output_path: Path,
    hook_count: int = 5,
    model: str = "gpt-4o-mini",
) -> Dict[str, object]:
    """Generate hooks, choose one, produce script, and build subtitle chunks.

    Returns:
        Dictionary containing hooks, selected hook, script, caption chunks, and
        generated ASS path.
    """
    hooks = generate_hooks(topic=topic, count=hook_count, model=model)
    if not hooks:
        raise RuntimeError("No hooks were generated.")

    # Simple strategy: pick the first generated hook.
    selected_hook = hooks[0]

    script = generate_script(hook=selected_hook, model=model)

    caption_chunks: List[CaptionChunk] = chunk_script(script)
    ass_content = build_ass_subtitles(caption_chunks)
    written_ass_path = write_ass_file(ass_content, ass_output_path)

    return {
        "hooks": hooks,
        "selected_hook": selected_hook,
        "script": script,
        "captions": caption_chunks,
        "ass_path": written_ass_path,
    }
