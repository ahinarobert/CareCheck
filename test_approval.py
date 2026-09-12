from unittest.mock import MagicMock

from hooks import require_caregiver_approval

fake_event = MagicMock()
fake_event.tool_use = {
    "name": "prepare_pharmacy_reorder",
    "input": {"medication_name": "Aspirin", "pharmacy_name": "CVS Pharmacy"},
}
fake_event.cancel_tool = None

require_caregiver_approval(fake_event)

print("\nFinal result -- cancel_tool is:", fake_event.cancel_tool)


