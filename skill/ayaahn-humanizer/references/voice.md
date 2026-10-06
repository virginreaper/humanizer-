# Humanizer voice reference

From the Humanizer design system. Use it after the script runs, and when writing fresh text for Ayaahn.

## Voice for product copy

- Write short, flat, declarative sentences. State what the tool does, then what it can't. "This is rule-based, not a language model. It removes patterns; it can't make dull writing good."
- Address the reader as **you**; the tool speaks as nobody. No "we", no "I", no mascot voice.
- Sentence case everywhere: headings, buttons, flags. Code, commands and flags are always in `mono`.
- No emoji, no decorative bold, no exclamation marks, no "Certainly!", no "Let's dive in".
- Be honest about limits in the same breath as the feature. Never promise to beat a detector.
- Say what is touched and what is not: "Code fences are never touched." "Vague attribution needs a real source or a human call."
- CLI output is terse lowercase key: value lines on stderr, for example `style: essay`.
- British spelling, curly quotes and the author's own dash style are preserved, never normalised.

### Words the tool removes

Never write these in product copy either: delve, tapestry, pivotal, crucial, vital, vibrant, intricate, meticulous, robust, seamless, holistic, comprehensive, leverage, harness, empower, elevate, navigate, ecosystem, nuanced, underscore, utilize, facilitate, myriad, plethora, cutting-edge, game-changer, unlock, unleash.

| Instead of | Write |
| --- | --- |
| in order to | to |
| due to the fact that | because |
| a wide range of | many |
| plays a pivotal role in | matters for |
| serves as | is |
| It's important to note that | (cut it) |
| In conclusion | (cut it) |

Also avoid: "Here's the thing", "To be clear", "Honestly?", "Read that again", flattery openers ("You're absolutely right"), hedge stacks ("could potentially"), "Despite these challenges... continues to thrive", "from X to Y" ranges with no real scale, and sentences that announce their own importance. Never add facts or invented personality when rewriting.

Also avoid: "not X, it's Y" framing, trailing "-ing" riders ("highlighting the importance of…"), forced triads, even sentence rhythm, a summary closer.

## The author's voice

Measured from `samples/` (7 pieces, about 2,500 words; run `python -m humanizer --learn` to refresh). When writing as the author, match these, not a generic style.

| | academic | essay | speech | personal |
| --- | --- | --- | --- | --- |
| Mean sentence length (words) | 37 | 26 | 21 | 19 |
| Contractions per 100 words | 0 | 1.0 | 1.8 | 1.6 |
| First person per 100 words | 0 | 4.3 | 10.3 | 10.0 |

- Sentences run long with wide variety (average 27 words, spread about 12). Keep short ones in between.
- Comma splices and run-ons are part of the voice. Do not fix them.
- Academic writing takes no contractions and no "I". Speeches and personal pieces are first person and use contractions.
- Dashes are spaced em dashes (` — `), ellipses are three plain dots, quotes are curly (93% of the time), spelling is British.
- About 1 sentence in 20 starts with And, But or So. Common openers: It, I, The, When, A, But.
- Questions are rare (none in the samples); exclamations are rare (about 1 sentence in 40).
- Phrases the author really uses, so never strip them: "at the end of the day", "to conclude", "utilize", "showcases".
