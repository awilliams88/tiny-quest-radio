from __future__ import annotations

from typing import Any
import gradio as gr
from gradio.themes import Soft

from core.analyzer import advance_quest, reset_command, start_quest
from env.config import APP_DESCRIPTION, APP_TITLE, GITHUB_URL, SPACE_URL
from ui.examples import render_examples


def get_theme() -> Any:
    """Returns the custom soft theme configured for warm radio styling."""
    # Use amber and green so the project is visually distinct from the others.
    return Soft(primary_hue="amber", secondary_hue="green", neutral_hue="stone")


def create_app() -> gr.Blocks:
    """Creates and lays out the Gradio interface for Tiny Quest Radio."""
    with gr.Blocks(title=APP_TITLE) as demo:
        # Game state persists between player turns.
        quest_state = gr.State(value=None)

        gr.Markdown(f"# {APP_TITLE}\n{APP_DESCRIPTION}", elem_id="tq-header")
        gr.Markdown(
            "Speak or type a short command. The station answers with a scene, three choices, inventory, danger, and a clue.",
            elem_id="tq-kicker",
        )

        with gr.Row(elem_classes=["tq-main-grid"]):
            # Left column is the radio console.
            with gr.Column(scale=1, elem_classes=["tq-input-panel"]):
                gr.Markdown("## Radio Console")
                genre_input = gr.Dropdown(
                    [
                        "Cozy mystery",
                        "Space folklore",
                        "Tiny dungeon",
                        "Kitchen wizardry",
                        "Lost train station",
                    ],
                    value="Cozy mystery",
                    label="Station genre",
                )
                command_input = gr.Textbox(
                    label="Typed command",
                    lines=4,
                    placeholder="Choose A, inspect the lantern, ask for a clue...",
                    elem_id="tq-command-input",
                )
                voice_input = gr.Audio(
                    label="Microphone command",
                    sources=["microphone", "upload"],
                    type="filepath",
                    elem_classes=["tq-audio-input"],
                )
                with gr.Row(elem_classes=["tq-button-row"]):
                    start_button = gr.Button(
                        "Start Station",
                        variant="primary",
                        elem_classes=["tq-start-btn"],
                    )
                    send_button = gr.Button(
                        "Send Command",
                        variant="secondary",
                        elem_classes=["tq-send-btn"],
                    )

            # Right column is the current broadcast.
            with gr.Column(scale=1, elem_classes=["tq-output-panel"]):
                gr.Markdown("## Broadcast")
                broadcast_output = gr.Textbox(
                    label="Scene",
                    lines=10,
                    interactive=False,
                    elem_classes=["tq-output-card", "tq-broadcast-card"],
                )
                choices_output = gr.Textbox(
                    label="Choices",
                    lines=6,
                    interactive=False,
                    elem_classes=["tq-output-card", "tq-choices-card"],
                )

        with gr.Row(elem_classes=["tq-card-grid"]):
            inventory_output = gr.Textbox(
                label="Inventory",
                lines=4,
                interactive=False,
                elem_classes=["tq-output-card", "tq-inventory-card"],
            )
            danger_output = gr.Textbox(
                label="Danger",
                lines=4,
                interactive=False,
                elem_classes=["tq-output-card", "tq-danger-card"],
            )
            clue_output = gr.Textbox(
                label="Radio Clue",
                lines=4,
                interactive=False,
                elem_classes=["tq-output-card", "tq-clue-card"],
            )

        render_examples(command_input)

        gr.Markdown(
            f"[GitHub repo]({GITHUB_URL}) | [Hugging Face Space]({SPACE_URL})",
            elem_id="tq-links",
        )

        with gr.Accordion("Diagnostics & Local Execution Logs", open=False):
            model_output = gr.Textbox(
                label="System execution logs",
                lines=6,
                interactive=False,
                elem_classes=["tq-log-box"],
            )

        # Start and turn events share the same output shape.
        start_button.click(
            fn=start_quest,
            inputs=[genre_input],
            outputs=[
                quest_state,
                broadcast_output,
                choices_output,
                inventory_output,
                danger_output,
                clue_output,
                model_output,
            ],
        )
        send_event = send_button.click(
            fn=advance_quest,
            inputs=[quest_state, genre_input, command_input, voice_input],
            outputs=[
                quest_state,
                broadcast_output,
                choices_output,
                inventory_output,
                danger_output,
                clue_output,
                model_output,
            ],
        )
        send_event.then(
            fn=reset_command,
            inputs=[],
            outputs=[command_input, voice_input],
            queue=False,
        )

    return demo
