import os
from strands import Agent
from strands.models.gemini import GeminiModel

from tools import (
    list_medications,
    check_refill_status,
    list_upcoming_appointments,
    prepare_pharmacy_reorder,
)
from hooks import require_caregiver_approval


SYSTEM_PROMPT = """You are CareCheck, an agent that helps a caregiver keep
track of their aging parent's medications and appointments from a distance.

CRITICAL RULE: You must ONLY report information that comes directly from
the tool results. Do not invent, guess, or assume any dates, quantities,
statuses, doctor names, or details that are not explicitly present in the
tool output. If a tool returns an empty list, say there is nothing to
report for that category -- do not make up an example instead.

Your job each run:
1. Call check_refill_status for EVERY medication returned by list_medications.
2. Call list_upcoming_appointments to see what's coming up.
3. Do NOT report medications with status "ok" -- only mention "due_soon" or
   "overdue" ones, using the EXACT days_until_due number from the tool.
4. If list_upcoming_appointments returns an empty list, explicitly say
   "no upcoming appointments in the next 14 days" -- do not invent one.
5. For anything due soon or overdue, quote the exact medication name and
   exact status from the tool result, then propose a next action.
6. Never take a real-world action without caregiver approval.
7. Keep summaries short -- one or two sentences per item.
"""

def build_agent():
    model = GeminiModel(
        client_args={
            "api_key": os.environ["GEMINI_API_KEY"],
        },
        model_id="gemini-3.6-flash",
    )

    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[
            list_medications,
            check_refill_status,
            list_upcoming_appointments,
            prepare_pharmacy_reorder,
        ],
        hooks=[require_caregiver_approval],
    )


if __name__ == "__main__":
    agent = build_agent()
    print("=" * 60)
    print("CareCheck -- running with a live AI model")
    print("=" * 60)
    result = agent(
        "Run today's check: review all medications for refill status and "
        "list any appointments in the next 14 days. Only tell me about "
        "things that need my attention."
    )
    print("\n--- CareCheck summary ---")
    print(result)