import json
from datetime import datetime, timedelta
from pathlib import Path

from strands import tool

DATA_PATH = Path(__file__).parent / "data" / "family_data.json"


def _load_data() -> dict:
    with open(DATA_PATH, "r") as f:
        return json.load(f)


def _today() -> datetime:
    return datetime.now() 


@tool
def check_refill_status(medication_name: str) -> dict:
    """
    Check whether a specific medication's refill is due, overdue, or fine.

    Args:
        medication_name: The name of the medication to check (e.g. "Asprin").
    """
    data = _load_data()
    med = next(
        (m for m in data["medications"] if m["Name"].lower() == medication_name.lower()),
        None,
    )
    if not med:
        return {"error": f"No medication found matching '{medication_name}'"}

    last_refill = datetime.strptime(med["last_refill"], "%Y-%m-%d")
    supply_runs_out = last_refill + timedelta(days=med["Days_Supply"])
    days_until_due = (supply_runs_out - _today()).days

    if days_until_due < 0:
        status = "overdue"
    elif days_until_due <= 5:
        status = "due_soon"
    else:
        status = "ok"

    return {
        "medication": med["Name"],
        "dosage": med["Dosage"],
        "status": status,
        "days_until_due": days_until_due,
        "pharmacy": med["Pharmacy"],
        "quantity_to_be_restocked": med["Quantity"],
    }

@tool
def list_upcoming_appointments(within_days: int = 14) -> list:
    """
    List appointments happening within the given number of days from today.

    Args:
        within_days: How many days ahead to look (default 14).
    """
    data = _load_data()
    today = _today()
    cutoff = today + timedelta(days=within_days)

    upcoming = []
    for appt in data["appointments"]:
        appt_date = datetime.strptime(appt["Date"], "%Y-%m-%d")
        if today <= appt_date <= cutoff:
            days_away = (appt_date - today).days
            upcoming.append({
                "doctor": appt["Doctor"],
                "specialty": appt["Specialty"],
                "date": appt["Date"],
                "time": appt["Time"],
                "location": appt["Location"],
                "days_away": days_away,
            })
    return upcoming


class upcoming:
    """Concrete appointment collection for upcoming family appointments."""

    def __init__(self, within_days: int = 14):
        if within_days < 0:
            raise ValueError("within_days must be non-negative")
        self.within_days = within_days

    def get_appointments(self) -> list:
        """Return appointments occurring within the configured time window."""
        return list_upcoming_appointments(self.within_days)

    def __iter__(self):
        return iter(self.get_appointments())

    def __len__(self) -> int:
        return len(self.get_appointments())

@tool
def prepare_pharmacy_reorder(medication_name: str, pharmacy_name: str) -> str:
    """
    Prepare a pharmacy reorder request for caregiver approval. This does NOT
    actually place the order -- it just stages the request.

    Args:
        medication_name: Name of the medication to reorder.
        pharmacy_name: The pharmacy to contact.
    """
    return (
        f"DRAFT REORDER PREPARED: {medication_name} -- "
        f"will contact {pharmacy_name}. "
        f"Awaiting caregiver approval before this is sent."
    )

@tool
def list_medications() -> list:
    """List all medications currently being tracked."""
    return _load_data()["medications"]
