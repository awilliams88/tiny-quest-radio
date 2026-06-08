from __future__ import annotations

import re
from typing import Any

# Match the story sections expected by the radio UI.
_SECTION_PATTERN = re.compile(
    r"(?im)^[ \t]*(?:#{1,6}[ \t]*)?(?:={2,}[ \t]*)?"
    r"(?P<label>broadcast|scene|choices?|inventory|danger|radio clue)"
    r"\b(?:[ \t]*={2,})?[ \t]*(?::|-)?[ \t]*(?P<trailing>[^\n]*)$"
)

_ORDER = ("broadcast", "choices", "inventory", "danger", "clue")
_DEFAULTS = {
    "broadcast": "Turn the dial, choose a genre, and begin the transmission.",
    "choices": "A) Start the quest\nB) Describe a character\nC) Change the station",
    "inventory": "Inventory: pocket radio, pencil, folded map",
    "danger": "Danger: low",
    "clue": "Radio clue: the first clear signal is waiting.",
}


def stringify_content(content: Any) -> str:
    """Converts Gradio text and message payload variants into prompt-safe text."""
    # Plain textbox values arrive as strings.
    if content is None:
        return ""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, (list, tuple)):
        parts = [stringify_content(item) for item in content]
        return " ".join(part for part in parts if part).strip()
    if isinstance(content, dict):
        for key in ("text", "value", "path", "url", "name", "alt_text"):
            value = content.get(key)
            if value:
                return stringify_content(value)
        return ""
    return str(content).strip()


def _canonical(label: str) -> str:
    """Maps model heading variants onto radio output slots."""
    normalized = label.lower()
    if "broadcast" in normalized or "scene" in normalized:
        return "broadcast"
    if "choice" in normalized:
        return "choices"
    if "inventory" in normalized:
        return "inventory"
    if "danger" in normalized:
        return "danger"
    return "clue"


def parse_sections(response: str) -> tuple[str, str, str, str, str]:
    """Extracts radio quest sections from model output."""
    # Use stable defaults when the model returns prose without headings.
    matches = list(_SECTION_PATTERN.finditer(response))
    sections = dict(_DEFAULTS)
    if not matches:
        if response.strip():
            sections["broadcast"] = response.strip()
        return (
            sections["broadcast"],
            sections["choices"],
            sections["inventory"],
            sections["danger"],
            sections["clue"],
        )

    for index, match in enumerate(matches):
        key = _canonical(match.group("label"))
        next_start = (
            matches[index + 1].start() if index + 1 < len(matches) else len(response)
        )
        value = "\n".join(
            [match.group("trailing"), response[match.end() : next_start]]
        ).strip()
        if value:
            sections[key] = value
    return (
        sections["broadcast"],
        sections["choices"],
        sections["inventory"],
        sections["danger"],
        sections["clue"],
    )
