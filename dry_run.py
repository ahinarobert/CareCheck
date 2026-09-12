from tools import list_medications, check_refill_status, list_upcoming_appointments
from state import dismiss_alert, is_dismissed_at_this_level

def decide_medication_actions() -> list:
    decisions = []
    for med in list_medications():
        status_info = check_refill_status(med["Name"])
        status = status_info["status"]

        if status == "ok":
            continue

        alert_key = f"medication:{med['Name']}"

        
        if status == "overdue":
            decisions.append({
                "type": "medication",
                "item": med["Name"],
                "urgency": "high",
                "alert_key": alert_key,
                "action": "reorder",
                "pharmacy": med["Pharmacy"],
                "message": f"{med['Name']} is {abs(status_info['days_until_due'])} day(s) overdue for refill.",
                "options": [
                    "Prepare a pharmacy reorder request",
                    "Just remind the parent directly",
                    "Mark as already handled",
                ],
            })    
            
        elif status == "due_soon":
            decisions.append({
                "type": "medication",
                "item": med["Name"],
                "urgency": "normal",
                "alert_key": alert_key,
                "action": None,
                "message": f"{med['Name']} refill is due in {status_info['days_until_due']} day(s).",
                "options": [
                    "Remind the parent now",
                    "Wait -- check again tomorrow",
                ],
            })

    return decisions


def decide_appointment_actions(within_days: int = 14) -> list:
    decisions = []
    for appt in list_upcoming_appointments(within_days=within_days):
        alert_key = f"appointment:{appt['doctor']}:{appt['date']}"

        urgency = "high" if appt["days_away"] <= 7 else "normal"
        decisions.append({
            "type": "appointment",
            "item": f"{appt['doctor']} ({appt['specialty']})",
            "urgency": urgency,
            "alert_key": alert_key,
            "action": None,
            "message": f"{appt['specialty']} appointment with {appt['doctor']} is in {appt['days_away']} day(s), at {appt['location']}.",
            "options": [
                "Confirm someone can take them",
                "No action needed yet",
            ],
        })
       

    return decisions

from tools import prepare_pharmacy_reorder


def ask_caregiver(message: str, options: list) -> str:
    print(f"\n{message}")
    print("   [y] Yes, proceed   [n] No, dismiss   [m] Maybe later, remind me tomorrow")
    answer = input("   Your choice: ").strip().lower()
    return answer


def handle_decision(d: dict):
    alert_key = d["alert_key"]
    urgency = d["urgency"]

    if is_dismissed_at_this_level(alert_key, urgency):
        return  # caregiver already said "no" at this exact urgency level

    icon = "🔴" if urgency == "high" else "🔵"
    print(f"\n{icon} [{d['type'].upper()}] {d['item']}")
    print(f"   {d['message']}")

    answer = ask_caregiver("What would you like to do?", d["options"])

    if answer == "y":
        if d["type"] == "medication" and d.get("action") == "reorder":
            result = prepare_pharmacy_reorder(d["item"], d.get("pharmacy", "the pharmacy"))
            print(f"   ✅ {result}")
        else:
            print("   ✅ Marked as confirmed/handled.")
        dismiss_alert(alert_key, urgency)

    elif answer == "n":
        print("   ❌ Dismissed. Won't ask again unless this gets more urgent.")
        dismiss_alert(alert_key, urgency)

    else:
        print("   ⏳ Okay, will remind you again tomorrow.")
        # deliberately NOT dismissing -- tomorrow is a new day, so it will
        # naturally ask again


def run_dry_check():
    all_decisions = decide_medication_actions() + decide_appointment_actions()

    print("=" * 60)
    print("CareCheck DRY RUN")
    print("=" * 60)

    if not all_decisions:
        print("Nothing to report today. Everything is on track.")
        return

    anything_shown = False
    for d in all_decisions:
        if not is_dismissed_at_this_level(d["alert_key"], d["urgency"]):
            anything_shown = True
        handle_decision(d)

    if not anything_shown:
        print("Nothing new to report today. Everything is on track.")


if __name__ == "__main__":
    run_dry_check()
