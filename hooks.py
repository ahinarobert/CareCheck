from strands.hooks import BeforeToolCallEvent

SENSITIVE_TOOLS = {"prepare_pharmacy_reorder"}


def require_caregiver_approval(event: BeforeToolCallEvent):
    tool_name = event.tool_use["name"]

    if tool_name not in SENSITIVE_TOOLS:
        return

    tool_input = event.tool_use.get("input", {})
    print(f"\n⚠️  CareCheck wants to run: {tool_name}({tool_input})")
    answer = input("   Approve this action? [y/n]: ").strip().lower()

    if answer != "y":
        event.cancel_tool = "Caregiver did not approve this action. Skipping."
        print("   ❌ Action cancelled by caregiver.\n")
    else:
        print("   ✅ Approved. Proceeding.\n")