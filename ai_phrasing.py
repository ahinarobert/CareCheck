"""
Uses a small local AI model to phrase already-correct decisions naturally.

Important design choice: the AI is NEVER asked to read raw data or figure
out facts itself -- it's only asked to reword facts we already know are
correct (computed by dry_run.py's tested logic). This makes even a small
model reliable, since there's very little room for it to invent anything.
"""

from strands import Agent
from strands.models.ollama import OllamaModel

_model = OllamaModel(
    host="http://127.0.0.1:11434",
    model_id="llama3.2:1b",
)


_phrasing_agent = Agent(
    model=_model,
    system_prompt=(
        "You add ONLY the words 'Heads up: ' or 'Urgent: ' to the front of "
        "a sentence you are given, and nothing else. You NEVER change any "
        "other word in the sentence. You NEVER remove or replace words like "
        "'overdue', 'due', numbers, or names. You output ONLY the sentence "
        "with the prefix added -- no explanation, no quotes, no repetition."
    ),
)


def phrase_decision(decision: dict) -> str:
    """
    Adds an urgency prefix to an already-correct message. The AI's job is
    now extremely narrow -- just choosing which of two fixed prefixes fits
    -- rather than rewording facts, which proved unreliable even for a
    small model.
    """
    prefix = "Urgent: " if decision.get("urgency") == "high" else "Heads up: "
    return f"{prefix}{decision['message']}"