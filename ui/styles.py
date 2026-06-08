from __future__ import annotations

# Gradio CSS overrides create a tabletop radio interface.
CUSTOM_CSS = """
body, .gradio-container {
    background-color: #10110a !important;
    color: #fafaf0 !important;
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}

#tq-header {
    text-align: center;
    margin: 0 auto 0.65rem auto;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
#tq-header h1 {
    color: #fbbf24 !important;
    font-size: 2.65rem !important;
    font-weight: 760 !important;
    letter-spacing: 0 !important;
}
#tq-header p {
    color: #bef264 !important;
    font-size: 1.08rem !important;
}
#tq-kicker {
    width: fit-content;
    max-width: 92%;
    margin: 0 auto 1.5rem auto;
    padding: 0.72rem 1.6rem !important;
    background-color: rgba(132, 204, 22, 0.08) !important;
    border: 1px solid rgba(251, 191, 36, 0.48) !important;
    border-radius: 8px !important;
    text-align: center;
    color: #fef3c7 !important;
}
.tq-main-grid, .tq-card-grid, .tq-example-grid, .tq-button-row {
    gap: 1rem !important;
    align-items: stretch !important;
}
.tq-main-grid > .form, .tq-main-grid > .row, .tq-main-grid > div,
.tq-card-grid > .form, .tq-card-grid > .row, .tq-card-grid > div,
.tq-example-grid > .form, .tq-example-grid > .row, .tq-example-grid > div {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 1rem !important;
}
.tq-input-panel, .tq-output-panel, .tq-examples-section, .tq-card-grid {
    background-color: #1c1a10 !important;
    border: 1px solid rgba(251, 191, 36, 0.24) !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3) !important;
    padding: 1.15rem !important;
}
.tq-examples-section, .tq-card-grid {
    margin-top: 1rem !important;
}
.tq-input-panel, .tq-output-panel {
    flex: 1 1 330px !important;
}
.tq-input-panel h3, .tq-output-panel h3, .tq-examples-section h3 {
    color: #fde68a !important;
    margin: 0 0 0.75rem 0 !important;
}
#tq-command-input textarea, .tq-log-box textarea, .tq-output-card textarea {
    background-color: #0f1009 !important;
    color: #fffbeb !important;
    border-radius: 8px !important;
    line-height: 1.55 !important;
    overflow-wrap: anywhere !important;
}
#tq-command-input textarea, .tq-log-box textarea {
    border: 1px solid rgba(190, 242, 100, 0.32) !important;
}
.tq-output-card {
    min-width: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
.tq-card-grid .block {
    flex: 1 1 240px !important;
    min-width: 0 !important;
}
.tq-broadcast-card textarea { border: 1px solid rgba(251, 191, 36, 0.5) !important; }
.tq-choices-card textarea { border: 1px solid rgba(163, 230, 53, 0.5) !important; }
.tq-inventory-card textarea { border: 1px solid rgba(45, 212, 191, 0.42) !important; }
.tq-danger-card textarea { border: 1px solid rgba(251, 113, 133, 0.42) !important; }
.tq-clue-card textarea { border: 1px solid rgba(96, 165, 250, 0.42) !important; }
.tq-start-btn {
    background: #fbbf24 !important;
    color: #10110a !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 760 !important;
    min-height: 50px !important;
}
.tq-send-btn {
    background: #84cc16 !important;
    color: #10110a !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 760 !important;
    min-height: 50px !important;
}
.tq-example-card {
    flex: 1 1 220px !important;
    background-color: #0f1009 !important;
    border: 1px solid rgba(251, 191, 36, 0.24) !important;
    border-radius: 8px !important;
    padding: 0.85rem !important;
}
.tq-example-copy strong {
    color: #bef264;
}
.tq-example-copy p {
    color: #fef3c7;
    margin: 0.35rem 0 0 0;
    line-height: 1.45;
}
#tq-links {
    text-align: center;
    margin-top: 1rem;
    color: #bef264 !important;
}
"""
