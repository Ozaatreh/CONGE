"""Hook generation utilities for YouTube Shorts psychology/facts content."""

from __future__ import annotations

from typing import List

from openai import OpenAI


SYSTEM_PROMPT = (
    "You generate short, punchy YouTube Shorts hooks about psychology and fascinating facts. "
    "Each hook must be under 12 words and feel curiosity-driven."
)


def generate_hooks(topic: str, count: int = 5, model: str = "gpt-4o-mini") -> List[str]:
    """Generate multiple hook lines for a given psychology/facts topic.

    Args:
        topic: Topic focus, e.g. "habit formation" or "dark psychology myths".
        count: Number of hooks to request from the model.
        model: OpenAI model name.

    Returns:
        A list of hook strings.
    """
    # Create API client (reads OPENAI_API_KEY from environment by default).
    client = OpenAI()

    # Ask for numbered hooks so parsing remains simple and deterministic.
    user_prompt = (
        f"Generate {count} short hook lines about: {topic}.\n"
        "Constraints:\n"
        "- Maximum 12 words each\n"
        "- Energetic and curiosity-focused\n"
        "- No hashtags\n"
        "Return as a numbered list."
    )

    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.9,
    )

    text = response.output_text.strip()
    hooks: List[str] = []

    # Parse numbered list output into clean hooks.
    for raw_line in text.splitlines():
        line = raw_line.strip().lstrip("-•")
        if not line:
            continue
        if "." in line and line.split(".", 1)[0].isdigit():
            line = line.split(".", 1)[1].strip()
        hooks.append(line)

    return hooks[:count]
