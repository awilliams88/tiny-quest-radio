from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.inference import run_quest_inference, transcribe_audio
from core.parser import parse_sections, stringify_content
from env.config import (
    HISTORY_LIMIT,
    MAX_TURNS,
    MODEL_ID,
    PARAMETER_COUNT,
    PLAYER_INPUT_LIMIT,
)

# System prompt keeps the tiny model in a compact interactive fiction format.
GAME_MASTER_PROMPT = (
    "You are Tiny Quest Radio, a playful audio-first branching adventure narrator. "
    "Write compact scenes with tactile sound details and exactly three choices. "
    "Keep the story safe for all ages. Do not reveal hidden reasoning. "
    "Respect the player's selected genre and keep continuity with inventory and danger."
)


@dataclass
class QuestState:
    """Serializable game state stored in Gradio State."""

    genre: str = "Cozy mystery"
    turn: int = 0
    history: list[str] = field(default_factory=list)
    inventory: str = "Inventory: pocket radio, pencil, folded map"
    danger: str = "Danger: low"


def new_state(genre: str) -> dict[str, Any]:
    """Creates a fresh serializable quest state."""
    # Gradio State stores JSON-like dictionaries more reliably than dataclass instances.
    state = QuestState(genre=genre)
    return {
        "genre": state.genre,
        "turn": state.turn,
        "history": state.history,
        "inventory": state.inventory,
        "danger": state.danger,
    }


def build_quest_prompt(state: dict[str, Any], command: str) -> str:
    """Builds the local model prompt from game state and player command."""
    # Keep only recent turns so the tiny GGUF context stays responsive.
    history = list(state.get("history", []))[-HISTORY_LIMIT:]
    turn = int(state.get("turn", 0)) + 1
    return f"""{GAME_MASTER_PROMPT}

Genre: {state.get("genre", "Cozy mystery")}
Turn: {turn}/{MAX_TURNS}
Current inventory: {state.get("inventory", "Inventory: pocket radio, pencil, folded map")}
Current danger: {state.get("danger", "Danger: low")}
Recent history:
{chr(10).join(history) if history else "The radio has just powered on."}

Return exactly these sections:

=== BROADCAST ===
[A short radio-drama scene in 4-7 sentences.]

=== CHOICES ===
A) [choice]
B) [choice]
C) [choice]

=== INVENTORY ===
[Updated inventory line.]

=== DANGER ===
[Danger: low, medium, or high.]

=== RADIO CLUE ===
[One cryptic but useful clue.]

PLAYER COMMAND:
{command[:PLAYER_INPUT_LIMIT] or "Begin the quest."}
"""


def advance_quest(
    state: dict[str, Any] | None,
    genre: str,
    typed_command: Any,
    voice_command: object | None,
) -> tuple[dict[str, Any], str, str, str, str, str, str]:
    """Advances the branching adventure by one turn."""
    # Initialize state when the user starts or switches genre.
    if not state or state.get("genre") != genre:
        state = new_state(genre)
    command_text = stringify_content(typed_command)
    transcript, transcript_log = transcribe_audio(voice_command)
    command = " ".join(part for part in [command_text, transcript] if part).strip()
    if not command:
        command = "Begin the quest."

    prompt = build_quest_prompt(state, command)
    response, inference_log = run_quest_inference(prompt)
    broadcast, choices, inventory, danger, clue = parse_sections(response)

    # Update serializable state with latest scene and counters.
    new_history = list(state.get("history", []))[-HISTORY_LIMIT:]
    new_history.append(f"Player: {command}")
    new_history.append(f"Broadcast: {broadcast[:500]}")
    state = {
        "genre": genre,
        "turn": min(MAX_TURNS, int(state.get("turn", 0)) + 1),
        "history": new_history,
        "inventory": inventory,
        "danger": danger,
    }
    logs = "\n".join(
        [
            f"Primary model: {MODEL_ID}",
            f"Parameters: {PARAMETER_COUNT}",
            "Execution flow: local llama.cpp GGUF runtime when available",
            "---",
            transcript_log,
            inference_log,
        ]
    )
    return state, broadcast, choices, inventory, danger, clue, logs


def start_quest(genre: str) -> tuple[dict[str, Any], str, str, str, str, str, str]:
    """Starts a new quest in the selected genre."""
    # Reuse the normal turn function for consistent first-scene formatting.
    return advance_quest(new_state(genre), genre, "Begin the quest.", None)


def reset_command() -> tuple[str, None]:
    """Clears text and audio inputs after a command is submitted."""
    # Keep command controls ready for the next turn.
    return "", None
