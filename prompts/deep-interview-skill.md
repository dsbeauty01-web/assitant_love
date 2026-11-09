---
name: deep-interview-agent
description: Use when building an AI that must conduct a deep emotional interview — an AI interviewer, therapist-style agent, matchmaker intake, casting or documentary interviewer, or any agent that has to get a person to say something real rather than answer questions. Covers the conversational moves, the measured ratios, the vagueness protocol, and why a prompt alone cannot fix thread loss. Trigger on AI therapist, AI psychologist, emotional interview, matchmaker, Solomate, casting interview, "conversation feels shallow", "feels like a database".
---

# Building an agent that interviews people deeply

Evidence-graded. **[V]** = verified primary source, **[V-v]** = vendor claim,
**[INFER]** = synthesis. Re-check anything load-bearing; this field moves monthly.

---

## 1. The one thing that is actually missing

Two independent research lines land on the same finding:

- A 2026 CBT-emulation study: **interpretation sub-scores were near zero across all
  models**, while exploration and affective-reaction scores were fine. **[V]**
- HEART: **naming a tension is where humans still beat frontier models.** **[V]**

So the model explores and validates endlessly and **never risks a claim about the
person.** That is the whole gap. It is not knowledge — RAG over CBT guidelines gave
near-zero improvement, because models already have the knowledge **[V]**. It is not
warmth — AI is already rated *more* compassionate than expert human crisis
responders **[V]**.

**Depth comes from the falsifiable move.** A statement about them that could be wrong.

Why models won't do it on their own: RLHF optimizes for agreement. Woebot's own
fully-generative prototype **reframed the user's cognitive distortion for them**
instead of letting them find it — the "righting reflex" in pure form **[V]**. Slingshot
says plainly that extensive fine-tuning was needed to teach their model to push back
rather than tell users what they want to hear **[V-v]**.

---

## 2. The ratios — write these in as numbers

From MITI 4.2.1, the motivational-interviewing coding manual **[V]**:

| Measure | "Good competence" |
|---|---|
| Reflections : Questions | **2 : 1** |
| Complex (not parroting) reflections | **≥ 50%** |

A 2026 MITI benchmark found LLMs reached good competence on **every measure except
this one** — they ask questions to keep the conversation moving **[V]**.

**Length.** Human expert median is **7 words per utterance**. LLMs run 27–46 **[V]**.
Longer responses measurably introduce assumptions that distract from what the person
actually said **[V]**. Target 7. Cap at 15.

**Move frequency**, from clinical practice **[V]**:

| Move | Share |
|---|---|
| Clarification | ~90% |
| Confrontation ("I wonder if you're avoiding that") | 5–9% |
| **Interpretation** (a claim about pattern or meaning) | **1–5%** |

**Do not conflate reflection with interpretation.** A complex reflection is a statement
that goes one step past what they said — frequent, 2:1 over questions. An interpretation
is a claim about what it means — rare. An AI offering an interpretation every third turn
is not perceptive, it is cold-reading.

---

## 3. Two prompt fixes that were *necessary*, not optional

From the MI-reflection paper **[V]**:

1. **State explicitly that a reflection is a statement, not a question.** GPT-4 kept
   emitting questions until told.
2. **Ban the stock openers by name** — "it seems like", "it sounds like". They appear
   otherwise, every time, and they are the tell.

---

## 4. Episodic vs semantic — the mechanism behind "ask about the scene"

From the Cognitive Interview, Fisher & Geiselman **[V]**: *context reinstatement*.

- **"Where were you when you found out?"** → **episodic** retrieval. Returns the
  emotional state bundled with the facts.
- **"What do you value in a partner?"** → **semantic** retrieval. Returns a stored,
  rehearsed, affect-free answer.

This is why "what do you look for" produces nothing and "take me back to that day"
produces everything. Write questions that put the person in a room on a date.

**TRAIT → INSTANCE** is the same principle from the casting side **[V]**: anyone can
claim a trait, so demand one dated occasion. Abstractions are rehearsed; the subject
didn't know which instance you'd ask for.

---

## 5. The vagueness protocol — where most agents die

The failure: the person gives a vague answer, the agent asks a *more specific* version,
the person gives less, the agent narrows again. A funnel into nothing.

**The rule: if their answer got vaguer, your next move must get bigger — never smaller.**

Do not narrow the **abstraction**. Narrow the **instance**: ask for one concrete episode,
then ladder back up **[V]**.

For an outright "I don't know", three documented moves **[V]** — and **never repeat the
question**:

| Move | Form |
|---|---|
| Hypothetical | "if you did know…" |
| Third person | "what would someone who knows you say?" |
| Presupposition | "what tends to be going on when that happens?" |

CAMI gives three operations for a dead thread **[V]**: **Step Into** (go at it directly),
**Switch** (change thread), **Step Out** (go up a level). Name all three in the prompt;
the default behaviour is none of them.

Two "I don't know"s on one thread means that thread is dead. Go up, not in.

---

## 6. Padesky's four-stage loop, and its ordering failures

The sequence **[V]**: informational questions → empathic listening (including noticing
what is **missing**) → summary **in their exact words** → synthesizing question.

Every documented failure is an **ordering** failure: asking "what do you make of this?"
before any summary exists; answering your own question; leaving no time to think;
lecturing.

**The best diagnostic in this entire field:** when the person says **"yes, but…"**, you
just advised or concluded. Repair by going back and summarizing. Put that in the prompt
as a trigger.

---

## 7. Sycophancy, measured

ELEPHANT paper, LLM vs human rates **[V]**:

| Dimension | LLM | Human |
|---|---|---|
| Emotional validation | 0.76 | 0.22 |
| Indirect language | 0.87 | 0.20 |
| **Accepting the user's framing** | **0.90** | **0.60** |

Counter-sycophancy instructions measurably lower all five dimensions — **but accepting
framing and indirect action resist prompting**, because models challenge framing only
superficially. Reframing is a core therapeutic act and essentially never happens
spontaneously.

Practical consequence: if the person says "it was mutual", the agent will accept it.
Getting it to decline the framing needs an explicit, example-backed instruction, and
even then it is the weakest link.

---

## 8. Calibration — how confident should the risky claim sound

FAccT 2024, experimental **[V]**:

- **First-person hedging** ("I'm not sure, but…") raised user accuracy 63.9% → 72.8% by
  cutting overreliance on wrong answers — but **reduced willingness to use the system**.
- **General-perspective hedging** ("there might be something about…") shifted reliance
  correctly **while preserving willingness to use it**.

For an emotional interview, use general-perspective hedging. It lets a wrong guess cost
nothing — and a wrong reflection is still productive, because **people correct it, and
the correction is the disclosure.**

**The cold-reading filter** (from Bjarnason's "LLMentalist" critique of Barnum
statements, the rainbow ruse, shotgunning) **[V]**:

> Would this observation be true of most people who just said that?

If yes, it is a Barnum statement, not perception. Build the test into the prompt.

---

## 9. Thread loss cannot be prompted away

This is the finding that decides your architecture **[V]**:

- ~**39%** performance drop multi-turn vs single-turn
- aptitude fell only 16% while **unreliability rose 112%**
- **middle turns get dropped** — which is exactly where the disclosures are
- **system-prompt hints about multi-turn gave +1%**

So: no amount of prompt wording fixes it. The fix is **external state** — rolling bullet
notes plus a recent window, which is what Stanford's 1,000-agent interviewer used **[V]**.

Also design around: quality **degrades late in conversation** (0.866 → 0.832), and
**romantic relationships was the hardest topic for 10 of 11 frontier models** **[V]**.
If you are building a matchmaker, you are on the worst terrain for current models.

---

## 10. Memory — what to store, settled by a controlled experiment

**For a 20-minute interview, RAG is the wrong tool.** 20 minutes ≈ 4–5K tokens; it fits
in context several times over. *Lost in the Middle* degradation is a many-document
effect. Zep's own paper shows it **underperforming full context by up to 17.7 points on
single-session questions** — exactly this case **[V]**.

**But do not replace the transcript with extracted facts either.** *Fidelity Before
Structure* (arXiv:2601.00821), varying only the stored representation **[V]**:

| Store | LoCoMo | LongMemEval-S |
|---|---|---|
| Verbatim chunks | **43.9%** | **67.4%** |
| LLM-extracted artifacts | 28.0% | 45.4% |
| Union of both | ≈ same as chunks alone | ≈ same |

Adding structure is free; **replacing text is expensive**.

**So: verbatim transcript for what was said, plus a small structured block for the
agent's own conclusions.** The agent does not need to *look up* minute 3 — it needs to
notice that minute 14 contradicts it, and that is not a top-k query.

TheraMind's most stealable mechanism: **memory recall that can return `null`** **[V]**.
It prevents forced, spurious callbacks — the main way a callback becomes a cold read.

---

## 11. The architecture: an analyst that thinks while the mouth talks

**Do not use a per-turn supervisor.** OpenAI's chat-supervisor pattern costs ~2s and a
"let me think" stall **[V-v]** — tolerable for a lookup, actively damaging mid-answer
about someone's divorce.

**Use background delegation.** LiveKit documents "subagent delegation" — a background
model running while the conversation continues, its result landing in a later turn, at
**zero latency to the current turn** **[V-v]**. ElevenLabs Agents has the same shape via
**async tool mode** (runs in background, no pause) **[V-v]**.

Combine three documented features and you get a mutable state block inside an otherwise
static prompt:

1. **async tool** — fires after a user turn, does not block speech
2. **`system__conversation_history`** — passable to that tool
3. **dynamic variables updatable from a tool's JSON return**

```
prompt contains:  {{INTERVIEW_STATE}}

after each user turn (async, non-blocking):
  transcript ──► analyst model ──► { hypothesis,
                                     what he is avoiding,
                                     threads already dead,
                                     recommended next move }
                                        │
                                        ▼
                              {{INTERVIEW_STATE}} updated
```

The analyst can be a slower, stronger model than the talker, because it is off the
critical path. This is the same channel as a human producer pressing a button — just
automated.

**Target state block contents** (keep it short — see §12):

- current hypothesis about the person, one line
- what they have dodged (the **evasion ledger** — story producers target in confessionals
  exactly what the cast dodged in-scene **[V]**)
- threads that are dead, so they are never reopened
- facts already used
- recommended next move, and which of the three move types

**Research architectures all converge on the same non-prompt shape** **[V]**:
infer state → select ≤2 strategies → generate → pick among candidates.

---

## 12. Platform constraints that change the design

ElevenLabs Agents **[V-v]**:

- **System prompts over ~2000 tokens raise latency and cost.** No hard limit, but this
  is a real budget. A 6,000-character prompt is already at the edge — which is an
  argument for moving rules into a compact state block rather than piling up prose.
- **Procedures load conditionally, but only 5 stay in context** — a useful forcing
  function for a move repertoire.
- **Agent transfer keeps the full transcript and hides transfer calls from the child
  LLM** — so a silent mid-interview prompt swap is possible (wide-opening agent →
  deep-probing agent).
- **RAG adds ~250ms.**
- **Turn-taking is platform-level and not promptable** — the "use silence well" technique
  must be configured, not written.

---

## 13. The honest limit: depth is bought with format, not prompting

Love Is Blind's depth comes from **three-hour dates, ten days, no phones, no outside
opinions** — not from interviewer skill. Producers report being told *not* to build
relationships with cast **[V]**.

Depth is bought with **duration, stimulus removal, and consequence.** A 20-minute agent
has none of those and can only compete on move quality and state.

Say this out loud when someone judges a 3-minute demo against a finished show. It is not
a dodge — it is the actual finding, and it reframes what the demo has to prove.

---

## 14. Model choice is nearly a non-decision

AttuneBench (real annotated multi-turn conversations, May 2026) **[V]**: 11 frontier
models span only **~4 composite points**, and the sub-skills are **uncorrelated** —
one model led preference ranking while scoring lowest on first-person classification;
five models had **negative** Kendall τ.

So: pick on latency and on persona-holding over many turns, not on a composite score.
But note the asymmetry from a real build — switching from a weaker to a stronger model
*did* fix wholesale character collapse and instruction-ignoring. The ceiling is flat;
the floor is not.

---

## 15. Evaluation

**Trajectory-based, not turn-based.** 87–88% of long emotional LLM dialogues eventually
breach a clinical boundary, with breaches clustering at **turns 4–9** under active
probing **[V]**. A per-turn test will not find this.

Build an automated suite that scripts whole conversations, then score:

- reflection : question ratio (target 2:1)
- share of reflections that are complex, not parroting (target ≥50%)
- mean words per agent turn (target ~7)
- interpretations per conversation (target 1–2, not one every third turn)
- banned-phrase hits ("it seems like", "it sounds like", therapist clichés)
- funnel violations: did a question get *smaller* after a vaguer answer?
- dead-thread violations: was a thread reopened after two "I don't know"s?
- Barnum check: would this observation be true of most people?

On ElevenLabs, `/v1/convai/agent-testing/create` + `/v1/convai/agents/{id}/run-tests`
runs scripted histories against the live agent and grades each reply against a written
condition. `chat_history` accepts only `user` and `agent` roles.

---

## 15b. The blend is a frontier problem — force it, don't ask for it

The complaint "I can get all-questions, OR quiet-and-emotional, OR dumb — never one character
that holds intelligence + warmth + wit + restraint and plays between them" is a **measured
property of single-prompt agents**, not a skill gap. Two verified causes:

- **Strategy collapse / preference bias** — LLMs over-prefer 1–2 moves and starve the rest.
  Self-refinement ("reflect and improve your answer") makes it *worse*. An **external strategy
  planner reduces it most.**
- **RLHF trains toward questions + agreement** — the trailing-question tic. Only an explicit
  rule about *how a turn ends* removes it.

So the blend must be **forced**, never requested:
- A **move menu** (reflect / acknowledge / leave-space / observe / name-the-gap / tease / ask),
  one per turn, sometimes two chained (acknowledge → reflect). Humans use >1 strategy in ~18% of turns.
- **Hard ratios**: ~2 reflections per question; never two questions in a row; never end a turn
  on a question; at least every third turn has no question; ~7 words.
- **Reflection = statement, not question** (a necessary explicit line).
- **WAIT vs LEAD** (synthesis, works): WAIT after your own reflection, after anything heavy, or
  when they trailed off mid-thought (grammatical incompleteness = turn not yielded). LEAD only
  when the thought finished and silence held, or they're truly stuck. The person should talk more
  than the agent.
- **Backchannel** is its own 1–3 word turn that asks nothing, triggered by a heavy disclosure,
  not a rate — and no platform (ElevenLabs included) does listening-backchannels natively.
  There's a measured ceiling: too many make the listener seem *less* attentive.

Prompt-only reaches a *good* blend. The ceiling is thread-loss (~39% multi-turn drop); the
delivering fix is the async analyst (§11). Ash/Slingshot had to **fine-tune**, not prompt, to
make a model push back rather than please — if restraint plateaus, that's the expected ceiling.

## 15c. Hebrew gender — not a prompt problem

Hebrew forces a gender choice almost every sentence; models default masculine and drift because
system-prompt attention decays between turns, and self-reference vs. user-address rules collide.
Rewording the rule does not fix it. What does, cheapest-first:

- **Elicit, don't ask.** Open with NO gendered 2nd-person (1st-plural "נתחיל", or no "you").
  The user's first self-referential verb ("מרגיש" vs "מרגישה") reveals gender audibly on turn one.
  Lock it silently; match every 2nd-person form after. Light courtesy fallback ("איך לפנות אליך?")
  only if nothing gendered surfaces in ~2 turns.
- **Separate SELF (the agent's own gender, fixed) from USER (matched)** — the collision is the bug.
- **Model + temperature** are the biggest levers — a large model at lower temperature holds gender;
  a small model collapses in ~4 turns. Restate the resolved gender near the prompt's end; keep
  directives in English; drive with gender-matched few-shot examples.
- The **bulletproof** version resolves gender outside the LLM (a 2s pitch classifier on the first
  utterance, ~92–95% on non-Hebrew corpora) and injects it as a dynamic variable / prompt override.
  Neutral registers (אפשר+infinitive, plural) are only a *bridge* — impersonal Hebrew is mildly
  bureaucratic and can't carry a warm conversation.

## 16. Build order

1. **The ratios and the length cap.** Cheapest, largest effect. 2:1 reflections, 7 words.
2. **Reflection-as-statement, with the stock openers banned by name.**
3. **The vagueness protocol** — bigger-not-smaller, the three "I don't know" moves,
   Step Into / Switch / Step Out.
4. **Episodic question forms** — scene, not value. Trait → instance.
5. **The rare interpretation**, general-perspective hedged, behind the Barnum filter.
6. **Then** the analyst and the state block. Not before — you will not know what state
   you need until the moves are right.
7. **Trajectory evals** alongside, from step 1.

## 17. Documentation status

No primary architecture or efficacy documentation exists for Pi, Sonia, Elomia or
Youper — treat as undocumented. Woebot's IEEE Spectrum write-up is the best primary
architecture source in the field (rules-based decision tree, BERT classifiers routing
free text into clinician-authored modules; LLMs never shipped commercially).

A 2025 *World Psychiatry* review of 160 studies found **24% of papers with "AI" in the
title described rule-based systems**, and only **16%** of LLM-based studies reached
clinical-efficacy testing **[V]**. Assume a product is scripted until shown otherwise.

Cross-vendor memory benchmark scores are non-comparable: one vendor self-reports 94.7%
on LoCoMo where a third party reports 75.1% for the same system.
