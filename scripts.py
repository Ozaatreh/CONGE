"""Script generation module for 20-30 second YouTube Shorts voiceover text."""

from __future__ import annotations

from typing import List

from openai import OpenAI


SYSTEM_PROMPT = (
    "You are a concise short-form scriptwriter for psychology/facts content. "
    "Write vivid, practical mini-scripts for spoken delivery."
)


def _word_count(text: str) -> int:
    return len([word for word in text.split() if word.strip()])


def _trim_to_max_words(text: str, max_words: int) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]).rstrip(" ,") + "."


def generate_script(hook: str, model: str = "gpt-4o-mini") -> str:
    """Generate a 45-65 word script from a hook.

    Args:
        hook: Hook line to expand.
        model: OpenAI model name.

    Returns:
        A compact script suitable for a 20-30 second short.
    """
    # Create API client (reads OPENAI_API_KEY from environment by default).
    client = OpenAI()

    prompt = (
        "Write a single YouTube Shorts script based on this hook:\n"
        f"\"{hook}\"\n\n"
        "Requirements:\n"
        "- 45 to 65 words\n"
        "- 20-30 second spoken pacing\n"
        "- Include one concrete psychology insight\n"
        "- Conversational tone, no bullet points\n"
        "- End with a one-line thought-provoking closer"
    )

    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
    )

    script = " ".join(response.output_text.split())

    # Keep output in requested length window as a safety guard.
    count = _word_count(script)
    if count > 65:
        script = _trim_to_max_words(script, 65)

    return script
