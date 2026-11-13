# HANDOFF — read this first

You are picking up a project with zero prior context. This file is everything you
need: what it is, where it lives, what's built, how to run it, and which keys to
set. Read it top to bottom before doing anything.

---

## 1. What this project is
A **Hebrew-language live voice agent** called **Solomate** for a TV format "AI LOVE"
(client: Elior Amsalem). An AI character interviews a dating-show guest live on
camera. There is a producer-control layer (secret director/camera instructions
injected mid-conversation) and a role-play frame (the tester plays "Avi," a
fictional 41-year-old divorced man).

Owner: Refael Sela (solo freelancer, **non-coder** — explain things plainly, no
jargon dumps). Respond to him in **English only**, even when content is Hebrew.

---

## 2. The repo — everything lives here
**GitHub (PUBLIC):** https://github.com/dsbeauty01-web/assitant_love

> PUBLIC repo = **never commit secret keys** into it. They get leaked and
> auto-disabled. Keys go in a local `.env` that is git-ignored (see section 6).

### File map
```
hub/index.html              Live demo page — single "Avi" agent
hub/compare.html            Live A/B page — sassy vs emotional (CURRENT page in use)
index.html                  Older root copy
prompts/solomate-prompt.txt The live system prompt (Hebrew) — the agent's brain
prompts/deep-interview-skill.md  The interview-craft research distilled (the "why")
second-brain/               Tier-2 async analyst (see section 5)
  director.py               The analyst webhook server
  test_director.py          Local test — run this to see the brain work
  tool_config.json          ElevenLabs Server Tool config
  README.md                 Second-brain setup steps
HANDOFF.md                  This file
```

### Live URLs (GitHub Pages, auto-served from `hub/`)
- A/B page (current): https://dsbeauty01-web.github.io/assitant_love/hub/compare.html
- Single demo:        https://dsbeauty01-web.github.io/assitant_love/hub/index.html

---

## 3. The ElevenLabs agents (IDs are not secret — the API key is)
Three agents exist in Refael's ElevenLabs account, wired into the pages above:

| Where | Personality | agent_id |
|---|---|---|
| index.html | Avi demo | `agent_5701m6qdcktme3a9ye6xwestr4xd` |
| compare.html | סאסית (sassy) | `agent_2901m6z66kqrfzkszym69q8h2sah` |
| compare.html | רגשית (emotional) | `agent_3601m6z66n15efkstd0gd1vcsm1q` |

Current agent settings (set in the ElevenLabs **dashboard**, not in code):
- TTS model: `eleven_v4_turbo` (Hebrew-capable; do NOT use Flash/Turbo v2.5)
- Voice: **Danit** (one of only 2 native-Hebrew female voices; the other is Zina)
- Brain/LLM: `claude-sonnet-5-5` (compare variants run on an Opus-5 brain)
- stability 0.40, temperature 0.75, turn: patient / 5s timeout / turn_v3
- Only valid audio tags: `[slowly] [pause] [softly]` — any invented tag gets read aloud

The full live prompt is `prompts/solomate-prompt.txt`. Editing the agent's actual
behavior is done in the **ElevenLabs dashboard → agent → System prompt**, and the
repo file is the source-of-truth copy. Keep them in sync by hand.

---

## 4. What's already built and working
- Two live, mic-enabled pages (above). Mic works because they're on HTTPS GitHub
  Pages — **mic does NOT work inside claude.ai artifacts**, so never move these there.
- The producer buttons: pages call ElevenLabs `sendContextualUpdate()` to inject
  `[במאי]`/`[מצלמה]` director/camera instructions mid-conversation.
- The prompt has been through several research rounds (gender-lock, forced
  conversation blend, escalation rules). See `prompts/deep-interview-skill.md`.

## 5. The Tier-2 "second brain" (newest piece, in `second-brain/`)
A separate small server (`director.py`) that reads the whole transcript and issues
one producer directive per turn automatically — gender-lock, dead-thread
escalation, anti-interrogation, emotion. It's wired to the live agent as an
ElevenLabs **Server Tool** (`tool_config.json`), which auto-injects the
conversation id + transcript via `system__conversation_id` /
`system__conversation_history`.

**Status: built + runs locally, NOT yet tested on camera, NOT yet tuned.**
Full setup is in `second-brain/README.md`. Verify it with
`python3 second-brain/test_director.py` before anything else.

---

## 6. Keys and environment — what to set

**The real key VALUES are not in this repo or workspace (by design).** Refael holds
them. Create a local `.env` (git-ignored) and fill in his values:

```bash
# .env  — DO NOT COMMIT. add ".env" to .gitignore first.
ELEVENLABS_API_KEY=xi-...        # from elevenlabs.io → Profile → API Keys
ANTHROPIC_API_KEY=sk-ant-...     # only needed to run second-brain/director.py (Haiku analyst)
# OPENAI_API_KEY=sk-...          # only if reusing any maya-lt TTS code; not needed for Solomate
```

Load it before running Python:
```bash
set -a; source .env; set +a
```

### Run each piece
```bash
# Dependencies
pip install flask requests

# 1. Test the second brain (needs ANTHROPIC_API_KEY)
python3 second-brain/test_director.py

# 2. Run the second-brain server (needs ANTHROPIC_API_KEY)
python3 second-brain/director.py          # http://localhost:8787
ngrok http 8787                            # public URL for ElevenLabs to reach

# 3. The live pages need no build — GitHub Pages serves hub/*.html automatically.
#    To change them: edit hub/*.html, git commit, git push. Pages updates in ~1 min.
```

---

## 7. Known limits / open loops (don't rediscover these the hard way)
- **Second brain adds latency** (~0.3–1.5s/turn, blocking call). Zero-latency needs
  ElevenLabs async-tool mode — a separate build, not done.
- **Gender agreement in Hebrew is genuinely hard** for the model; prompt rules help
  but aren't bulletproof. The second brain's gender-lock is the real fix, untested live.
- **Second-brain directives are an untuned first draft.** Expect a few rounds of
  tuning against real conversations, same as the live prompt took.
- Don't demo anything unattended. Test on yourself first.

---

## 8. How Refael wants to work
- He's non-technical. Explain in plain words, short. One clear next step at a time.
- Don't burn tokens. Be direct about what's done vs. what's left and who has to do it.
- Be honest, not flattering. If something isn't finished or won't work, say so.
