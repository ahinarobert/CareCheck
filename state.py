import json
from pathlib import Path
from datetime import datetime

STATE_PATH = Path(__file__).parent / "data" / "alert_state.json"


def _load_state() -> dict:
    if not STATE_PATH.exists():
        return {"alerted": {}}
    with open(STATE_PATH, "r") as f:
        return json.load(f)


def _save_state(state: dict):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def already_alerted_today(key: str) -> bool:
    state = _load_state()
    last_alert_date = state["alerted"].get(key)
    return last_alert_date == datetime.now().strftime("%Y-%m-%d")


def mark_alerted(key: str):
    state = _load_state()
    state["alerted"][key] = datetime.now().strftime("%Y-%m-%d")
    _save_state(state)


def dismiss_alert(alert_key: str, urgency_level: str):
    """Record that the caregiver dismissed this alert at a specific urgency level."""
    state = _load_state()
    state.setdefault("dismissed", {})[alert_key] = urgency_level
    _save_state(state)


def is_dismissed_at_this_level(alert_key: str, current_urgency: str) -> bool:
    """
    Check if this alert was already dismissed AT THIS SAME urgency level.
    If the urgency has gotten worse since it was dismissed, this returns
    False, so the alert correctly resurfaces.
    """
    state = _load_state()
    dismissed_at = state.get("dismissed", {}).get(alert_key)
    return dismissed_at == current_urgency