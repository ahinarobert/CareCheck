from flask import Flask, render_template, request, redirect

from dry_run import decide_medication_actions, decide_appointment_actions
from state import is_dismissed_at_this_level, dismiss_alert
from tools import prepare_pharmacy_reorder

app = Flask(__name__)


def get_visible_decisions():
    all_decisions = decide_medication_actions() + decide_appointment_actions()
    visible = []
    for d in all_decisions:
        if not is_dismissed_at_this_level(d["alert_key"], d["urgency"]):
            visible.append(d)
    return visible


@app.route("/")
def home():
    decisions = get_visible_decisions()
    message = last_message["text"]
    last_message["text"] = None  # clear it after showing once
    return render_template("index.html", decisions=decisions, message=message)

last_message = {"text": None}


@app.route("/respond", methods=["POST"])
def respond():
    choice = request.form.get("choice")
    alert_key = request.form.get("alert_key")
    urgency = request.form.get("urgency")
    item = request.form.get("item")
    action = request.form.get("action")
    pharmacy = request.form.get("pharmacy")

    if choice == "y":
        if action == "reorder":
            prepare_pharmacy_reorder(item, pharmacy)
            last_message["text"] = f"✅ Reorder request prepared for {item} at {pharmacy}."
        else:
            last_message["text"] = f"✅ {item} marked as confirmed."
        dismiss_alert(alert_key, urgency)
    elif choice == "n":
        last_message["text"] = f"❌ Dismissed {item}."
        dismiss_alert(alert_key, urgency)
    else:
        last_message["text"] = f"⏳ Will remind you about {item} again tomorrow."

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)