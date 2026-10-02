---
name: ayaahn-humanizer
description: Humanize text so it reads like Ayaahn wrote it. Use whenever the user pastes or attaches text and says humanize, make it sound human, remove AI tells, rewrite in my style, or asks to run text through the humanizer. Also use when a draft Claude just wrote for Ayaahn should be passed through it before delivery. Works on essays, speeches, assignments, articles, messages.
---

# Ayaahn's humanizer

A rule-based rewriter plus a style profile learned from Ayaahn's own writing
(academic paper, essays, speeches, personal piece). It strips AI patterns and keeps
meaning, content, tone, British spelling, curly quotes and his dash/ellipsis habits.
It does not "fix" his comma splices or run-ons on purpose, those are his voice.

## Steps

1. Save the user's text to `/tmp/in.txt` (pasted text) or use the attached file.
2. Run: `python scripts/run.py /tmp/in.txt > /tmp/out.txt` (paths relative to this skill folder).
   - It auto-picks the closest style: `academic`, `essay`, `speech` or `personal`.
     If the pick looks wrong for the piece (e.g. a legal paper treated as `essay`), rerun with
     `--register academic`.
   - The stderr line shows the style used, score before/after, and anything it could only flag.
3. Read `/tmp/out.txt` yourself. Fix what a script can't:
   - Vague attribution ("studies show") and lists of three: name a source if the user gave one, else
     leave the claim as is and tell the user it needs a source.
   - Anything that reads stiff or changed the meaning. Meaning and facts must not change.
   - Apply the rules in the user's existing humanizer skill (banned vocabulary, no negative
     parallelism, uneven sentence rhythm, no summary closer) on top, silently.
4. Reply with the final text. At most one short line on what it flagged. No lecture, no
   before/after table unless asked.

## Rules

- Never add facts, never drop content, never change the user's argument or opinion.
- Keep formal pieces formal (no contractions in `academic`), keep casual pieces casual.
- If the text is short (under ~40 words), skip the script and just rewrite by hand in his style.
- To update the profile, the user adds new writing to `samples/<register>/` in the GitHub repo
  virginreaper/humanizer- and rebuilds the skill.

## Design system

The voice rules this skill applies (banned vocabulary, plain replacements, structures to avoid, tone for any
product copy) are written up in the Humanizer design system: https://claude.ai/artifact/RHsQTRdybu3Gnt7HNyzuAd
Read its `project/README.md` when writing copy for this tool, and keep both in step when the pattern lists in
`scripts/humanizer/patterns.py` change.
