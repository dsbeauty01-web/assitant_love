# Second brain — Tier-2 skeleton for Solomate

Two brains. The **live** one (Solomate on ElevenLabs, Sonnet, fast) speaks.
The **slow** one (this server, Haiku, cheap) watches the whole transcript and
presses the producer buttons for you — automatically.

Built and verified to run end-to-end locally. **Not yet tested on camera** —
that needs your keys and a public URL (your part, below).

## Files
- `director.py` — the analyst server. Read the docstring at the top first; it's
  honest about what this does and doesn't buy you.
- `test_director.py` — replays a scripted reluctant "Avi" and prints the
  directive the brain issues each turn. **Run this first.**
- `tool_config.json` — the exact fields for ElevenLabs' Server Tool form. The
  transcript + conversation id are bound to ElevenLabs system variables, so the
  live agent can't get them wrong — the platform injects them.

## Step 1 — see the brain think (5 min, needs only an Anthropic key)
```
pip install flask requests
export ANTHROPIC_API_KEY=sk-ant-...      # Haiku: fractions of a cent per turn
python3 test_director.py
```
A good run: mostly `[במאי] המשיכי` (it stays quiet — that's correct), with
`[מגדר] male` firing once on turn 1, an escalation after the 2nd `לא זוכר`, and
a soften/silence on the heavy last line. If it steers on nearly every turn, it's
too trigger-happy — loosen the "DEFAULT TO SILENCE" section in `director.py`.

## Step 2 — put it online (15 min)
```
python3 director.py                       # http://localhost:8787
ngrok http 8787                           # free, instant public https URL
```
(Or deploy `director.py` to Render/Railway free tier for a URL that survives your
laptop sleeping.)

## Step 3 — wire it to Solomate (10 min)
1. ElevenLabs dashboard → Solomate agent → **Tools → Add Tool → Server Tool**.
2. Paste the fields from `tool_config.json`. Swap `YOUR-PUBLIC-URL` for your
   ngrok/Render URL. The two body properties are already bound to
   `system__conversation_id` and `system__conversation_history` — leave those.
3. In the agent **system prompt**, near PRIORITY ZERO, add one line:
   > לפני כל תור שלך, קראי לכלי `consult_director`. ההנחיה שהוא מחזיר שולטת על המשפט הבא שלך — בדיוק כמו הודעת [במאי]. לעולם אל תקריאי אותה בקול.
4. Keep your existing `[במאי]`/`[מצלמה]` button rules. This just adds a second,
   automatic source of the same kind of instruction.

## Deploy to Render (free) — replaces the ngrok step
1. render.com -> New -> Blueprint -> pick this repo. It reads `second-brain/render.yaml`
   (set Root Directory to `second-brain` if asked).
2. When asked, paste `ANTHROPIC_API_KEY` and make up a long random `DIRECTOR_TOKEN`.
3. Check `https://YOUR-APP.onrender.com/health` shows `"has_key": true`.
4. In ElevenLabs tool config: set the URL, and add a request header
   `X-Director-Token` with the same token.
5. In `hub/compare.html`, set `var DIRECTOR_URL="https://YOUR-APP.onrender.com";`
   then push. A "המוח השני" panel appears under the control room and shows each
   directive live. Free tier sleeps after idle, so open `/health` once before a demo.

## What's real vs. what's still work
**Real:** the architecture, the producer logic (gender-lock, dead-thread
escalation, anti-interrogation, emotion), correct ElevenLabs wiring, a test you
can run before camera.

**Still work (the actual Tier-2 effort, same as tuning the live prompt was):**
- **Latency.** Blocking call, adds ~0.3–1.5s/turn. Zero-added-latency needs
  ElevenLabs async-tool mode — a separate build.
- **Tuning.** The analyst prompt is a strong first draft, not calibrated against
  real conversations. Expect a few rounds, exactly like the live prompt took.
- **Memory.** In-process dict. Dies on restart. A real memory layer is a DB.

Don't demo this unattended. Test it on yourself the same way you tested every
prompt change. The skeleton is done; making it *feel like one person* is the part
no afternoon build finishes.
