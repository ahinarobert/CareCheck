# CareCheck

An autonomous agent built with the Strands Agents SDK that helps caregivers
manage an aging parent's medication refills and upcoming appointments from a
distance — without needing to repeatedly call and ask "did you take care of
this yet?"

## The problem

Caregivers managing a parent's care remotely currently do this through phone
calls and mental checklists: "did you refill your prescription?", "do you
have an appointment coming up?" It's tedious, easy to forget, and creates a
weekly cycle of nagging and uncertainty.

## What CareCheck does

- Tracks medication refill cycles and flags when a prescription is due soon
  or overdue
- Tracks upcoming appointments and flags ones happening soon
- Stays silent when everything is fine -- no unnecessary notifications
- Asks the caregiver a real yes/no/maybe-later question for anything that
  needs attention, instead of just displaying a status update
- Remembers what's already been handled, so it doesn't repeat the same
  alert -- but will resurface something if it becomes more urgent (e.g. a
  dismissed "due soon" medication that later becomes "overdue")
- Any real-world action (like preparing a pharmacy reorder) is gated behind
  explicit caregiver approval before it happens

## How it's built

- `tools.py` -- the individual capabilities: checking medication refill
  status, listing upcoming appointments, and preparing (but not sending) a
  pharmacy reorder request
- `hooks.py` -- an approval gate that intercepts any sensitive action and
  requires explicit caregiver confirmation before it proceeds
- `state.py` -- persistent memory that tracks what's already been
  surfaced/dismissed, and at what urgency level, so alerts don't repeat
  unnecessarily but do resurface when something gets worse
- `dry_run.py` -- the decision logic that ties everything together into one
  coordinated daily check, including the actual yes/no/maybe-later
  conversation with the caregiver
- `demo_timeline.py` -- lets us simulate different dates, since a real
  medication refill cycle plays out over 30-90 days, which can't be shown
  live in a short demo video

## Current status

The full system is built, tested, and running live:

**Rule-based core:** Decision logic in `dry_run.py` is thoroughly tested,
including edge cases like malformed data, duplicate-alert prevention, and
the approve/decline/dismiss-until-worse behavior — this is the "ground truth"
that all AI output is verified against.

**Live AI agent:** Connected to Google Gemini (`gemini-3.6-flash`) via the
Strands Agents SDK. All tool calls are verified accurate against real data
(zero hallucination observed). The agent correctly identifies medications
due soon/overdue and upcoming appointments, proposes specific next actions,
and respects the caregiver approval hook before any real-world action.

**Visual interface:** Web-based UI (Flask) lets caregivers interact with
CareCheck through a browser — see alerts as color-coded cards, click
Yes/No/Maybe Later buttons, get immediate confirmation feedback. All
dismissal and urgency-escalation logic works end-to-end through the visual
interface.

**Tested accuracy:** AI agent output verified rigorously against ground-truth
tool output — all medication statuses, appointment dates, and urgency levels
match real data exactly, no invented information.

## Roadmap (Post-Hackathon)

- Deploy to AWS Bedrock AgentCore (currently running on Gemini free tier)
- Real calendar integration (currently reads from local structured data)
- Appointment scheduling (currently tracks existing appointments only, not
  booking new ones)
- Push notifications (currently web/terminal UI only)

## Built with

- [Strands Agents SDK](https://strandsagents.com)
- Python 3.11