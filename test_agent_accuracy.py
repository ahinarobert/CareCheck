"""
Compares the AI agent's claims against the actual ground-truth tool output.
Run this after the agent responds, to objectively check for hallucination
instead of just trusting how confident the response sounds.
"""

from tools import check_refill_status, list_upcoming_appointments

print("=" * 60)
print("GROUND TRUTH (the actual correct data)")
print("=" * 60)

for med_name in ["Aspirin", "Metformin", "Paracetamol"]:
    print(check_refill_status(med_name))

print()
print(list_upcoming_appointments())

print()
print("=" * 60)
print("Now compare the above, line by line, against what agent.py said.")
print("Any medication/date/status the AI mentioned that doesn't appear")
print("exactly above is a hallucination.")
print("=" * 60)