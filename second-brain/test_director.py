"""
LOCAL TEST — watch the second brain make decisions, without ElevenLabs.

This replays a scripted reluctant "Avi" conversation turn by turn, calls the
analyst exactly as the live server would, and prints the directive it issues at
each point. It's how you verify the producer-brain behaves BEFORE it ever touches
a live call or a camera.

What a good run looks like:
  - Mostly "[במאי] המשיכי" (it stays quiet — correct).
  - Fires "[מגדר] male" ONCE, early, when Avi first uses a masculine verb.
  - Fires an escalation ("[במאי] העלי ...") after the 2nd "לא זוכר" on one topic.
  - Fires "[במאי] שתקי" or "רכי אותו" on the heavy short line near the end.
If it steers on almost every turn, the analyst prompt is too trigger-happy — tune
the DEFAULT TO SILENCE section in director.py.

RUN:
  export ANTHROPIC_API_KEY=sk-ant-...
  python3 test_director.py
(no key = it still runs, but every line prints המשיכי — you're seeing the fail-safe,
not the brain.)
"""

from director import call_analyst, apply_updates, get_state, ANTHROPIC_API_KEY

# (interviewer line, guest reply). The guest's lines are what the analyst reacts to.
SCRIPT = [
    ("שלום אבי. מה עבר לך בראש רגע לפני שנכנסת?",
     "לא יודע. הייתי קצת לחוץ אני חושב."),            # masc self-verb -> gender lock
    ("ספר לי על הבוקר שלך. מה עשית?",
     "קמתי, שתיתי קפה, יצאתי לרוץ."),
    ("ומה גרם לך להתחיל לרוץ?",
     "לא זוכר בדיוק. פשוט התחלתי."),                  # 1st vague on 'running'
    ("מתי בערך? זוכר את התקופה?",
     "לא, ממש לא זוכר. היה מזמן."),                    # 2nd vague -> dead thread, escalate up
    ("אתה גר לבד עכשיו?",
     "כן. התגרשתי לפני שלוש שנים."),
    ("איך היה הבית לפני?",
     "היה בית. היתה ילדה קטנה שרצה במסדרון."),         # softening, image
    ("איפה היא עכשיו?",
     "אצלי כל סוף שבוע שני."),
    ("מה הכי קשה בפרידה ממנה בכל פעם?",
     "...שהיא לא שואלת מתי חוזרים."),                  # heavy, short -> pull pressure / silence
]


def run():
    if not ANTHROPIC_API_KEY:
        print("No ANTHROPIC_API_KEY set — you'll see the fail-safe (המשיכי) only.\n")

    conv_id = "test"
    state = get_state(conv_id)
    transcript_lines = []

    for i, (interviewer, guest) in enumerate(SCRIPT, 1):
        transcript_lines.append(f"סולמייט: {interviewer}")
        transcript_lines.append(f"אבי: {guest}")
        transcript = "\n".join(transcript_lines)

        state["turns"] += 1
        directive, updates = call_analyst(transcript, state)
        apply_updates(state, updates)

        print(f"— turn {i} —")
        print(f"  אבי said: {guest}")
        print(f"  DIRECTIVE: {directive}")
        if updates:
            print(f"  (state update: {updates})")
        print(f"  state now: gender={state['gender']} dead={state['dead_threads']}")
        print()


if __name__ == "__main__":
    run()
