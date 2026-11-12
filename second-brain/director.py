"""
SECOND BRAIN — Tier-2 analyst server for the Solomate interview agent.

ARCHITECTURE (two brains):
  - LIVE brain  = Solomate on ElevenLabs (Sonnet, fast). Speaks. One job: say the
                  next line well, right now.
  - SLOW brain  = this server (Haiku, cheap). Doesn't speak. Watches the whole
                  transcript and, once per turn, issues ONE producer directive —
                  exactly the kind of thing you pressed by hand with the
                  [במאי]/[מצלמה] buttons. Now a model decides when to press.

The live agent calls this as a Server Tool at the start of each turn. ElevenLabs
injects the real conversation id and full transcript automatically (bound to
system__conversation_id / system__conversation_history in tool_config.json — the
LLM never fills these, so it can't get them wrong). This server returns a short
directive string, which the live prompt treats like a producer message.

THE DISCIPLINE THAT MATTERS: the analyst is SILENT most turns. It returns
"[במאי] המשיכי" (keep going, no change) unless there is a clear reason to steer.
A producer who talks every turn ruins the interview — that was the whole lesson
from the over-steering / strategy-collapse research. This brain earns its keep
by catching the 4 things a single live model reliably drifts on over a long
conversation:
  1. GENDER   — locks his/her grammatical gender from his own first verb form,
                once, so a mid-talk correction can't lose to a stale prompt rule.
  2. DEAD THREAD — two vague/"don't know" answers on one topic = escalate UP,
                and mark it dead so she never circles back (the "database"/funnel
                feeling Elior flagged).
  3. INTERROGATION — if her recent turns were mostly questions, force a statement
                or a silence (the "she doesn't leave space" problem).
  4. EMOTION  — if his last line is short/painful, pull pressure off.

Honest limits (unchanged from the skeleton — read before you demo this):
  - Adds latency. This is a blocking call, ~0.3-1.5s on Haiku. "Async, zero added
    latency" needs ElevenLabs async-tool mode wired separately.
  - State is in-memory. Dies on restart, one conversation at a time cleanly.
    Fine for a demo; a real memory layer is a database.
  - Untested on camera. Verified with test_director.py (see that file), not yet
    against a live ElevenLabs call. Test with yourself first.

RUN IT:
  pip install flask requests
  export ANTHROPIC_API_KEY=sk-ant-...        # Haiku, fractions of a cent per turn
  python3 director.py                         # http://localhost:8787
  ngrok http 8787                             # public URL for ElevenLabs to reach
"""

import os
import re
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANALYST_MODEL = "claude-haiku-4-5"   # the SLOW brain is small on purpose

# ---------------------------------------------------------------------------
# STATE — in-memory, per conversation. Swap for a DB if it must survive restart.
# ---------------------------------------------------------------------------
STATE = {}

def get_state(conv_id):
    if conv_id not in STATE:
        STATE[conv_id] = {
            "gender": None,        # "male" / "female" / None(unresolved)
            "dead_threads": [],    # topics killed by 2x vague answers
            "facts_used": [],      # briefed facts already spent (max 2 total)
            "turns": 0,
        }
    return STATE[conv_id]


# ---------------------------------------------------------------------------
# THE ANALYST PROMPT — the tuned producer logic, grounded in the interview
# research (move menu, ratios, escalation, gender-lock, facts-as-doors).
# ---------------------------------------------------------------------------
ANALYST_SYSTEM_PROMPT = """You are the SILENT PRODUCER of a live Hebrew TV love-interview.
You never speak on camera. You watch the transcript and the state, and you output
ONE directive for the interviewer's next line — nothing else.

DEFAULT TO SILENCE. If nothing clearly needs steering, output exactly:
DIRECTIVE: [במאי] המשיכי
A producer who interferes every turn destroys the interview. Most turns = המשיכי.
You interfere only for one of the four triggers below, and only when it clearly fires.

TRIGGER 1 — GENDER (highest priority).
If state gender is null AND the guest has just used a gendered self-referential verb
or adjective (Hebrew marks gender on these), lock it. Output:
DIRECTIVE: [מגדר] male        (or female)
STATE: gender=male            (or female)
Do this ONCE. If state gender is already set, never touch gender again.

TRIGGER 2 — DEAD THREAD (the "database"/funnel feeling).
If the current topic has gotten two vague / "לא יודע" / "לא זוכר" / shrug answers,
the thread is dead. Do NOT narrow, do NOT ask a smaller version. Escalate UP:
DIRECTIVE: [במאי] העלי — <2-4 words naming the bigger thing to reach, e.g. "לאקס", "לבת", "למה שמתחת">
STATE: dead=<one-word topic>
Never send her back to a topic already in state.dead_threads.

TRIGGER 3 — INTERROGATION (she doesn't leave space).
If her last two on-camera turns were both questions, force a non-question:
DIRECTIVE: [במאי] שתקי        (if his last line was heavy — say nothing, let it sit)
or
DIRECTIVE: [במאי] שקפי        (reflect: one statement that goes one step past his words, no question mark)

TRIGGER 4 — EMOTION.
If his last line is short and painful, or he's clearly moved:
DIRECTIVE: [מצלמה] דומע       (he's tearing up — stop asking, one line, wait)
or
DIRECTIVE: [במאי] רכי אותו    (drop the pressure, something small)

RULES:
- Output the DIRECTIVE line always. Output a STATE line ONLY when locking gender or
  killing a thread. No other text, ever. No explanation.
- The directive tag plus at most 4 Hebrew words. Short.
- You are not the interviewer. You never write her actual sentence — only the tag.
"""


def call_analyst(transcript, state):
    """Returns (directive_for_elevenlabs, state_updates_dict)."""
    if not ANTHROPIC_API_KEY:
        return "[במאי] המשיכי", {}          # no key -> safe no-op, never break the live call

    state_block = (
        f"gender: {state['gender']}\n"
        f"dead_threads: {state['dead_threads']}\n"
        f"facts_used: {len(state['facts_used'])}/2\n"
        f"turn: {state['turns']}"
    )
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": ANALYST_MODEL,
                "max_tokens": 60,
                "temperature": 0.2,            # steady, not creative — it's a referee
                "system": ANALYST_SYSTEM_PROMPT,
                "messages": [{
                    "role": "user",
                    "content": f"STATE:\n{state_block}\n\nTRANSCRIPT SO FAR:\n{transcript}\n\nYour output:",
                }],
            },
            timeout=6,
        )
        resp.raise_for_status()
        text = resp.json()["content"][0]["text"].strip()
    except Exception as e:
        print(f"[director] analyst call failed: {e}")
        return "[במאי] המשיכי", {}           # fail safe

    return parse_analyst_output(text)


def parse_analyst_output(text):
    """Pull the DIRECTIVE line (sent to ElevenLabs) and any STATE line (kept server-side)."""
    directive = "[במאי] המשיכי"
    updates = {}
    for line in text.splitlines():
        line = line.strip()
        if line.upper().startswith("DIRECTIVE:"):
            directive = line.split(":", 1)[1].strip()
        elif line.upper().startswith("STATE:"):
            body = line.split(":", 1)[1].strip()
            m = re.match(r"gender\s*=\s*(male|female)", body, re.I)
            if m:
                updates["gender"] = m.group(1).lower()
            m = re.match(r"dead\s*=\s*(\S+)", body, re.I)
            if m:
                updates["dead"] = m.group(1)
    return directive, updates


def apply_updates(state, updates):
    if "gender" in updates and state["gender"] is None:
        state["gender"] = updates["gender"]
    if "dead" in updates and updates["dead"] not in state["dead_threads"]:
        state["dead_threads"].append(updates["dead"])


# ---------------------------------------------------------------------------
# ENDPOINTS
# ---------------------------------------------------------------------------
@app.route("/director", methods=["POST"])
def director():
    payload = request.get_json(force=True) or {}
    conv_id = payload.get("conversation_id", "default")
    transcript = payload.get("transcript", "") or ""

    state = get_state(conv_id)
    state["turns"] += 1

    directive, updates = call_analyst(transcript, state)
    apply_updates(state, updates)

    print(f"[director] turn {state['turns']} | gender={state['gender']} "
          f"| dead={state['dead_threads']} | -> {directive}")

    # ElevenLabs stores this response; the live prompt reads {{directive}} as a
    # producer message for the next line.
    return jsonify({"directive": directive})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "has_key": bool(ANTHROPIC_API_KEY),
                    "conversations": len(STATE)})


if __name__ == "__main__":
    print("Second brain on http://localhost:8787  (POST /director, GET /health)")
    app.run(host="0.0.0.0", port=8787)
