# humanizer

Strips the usual AI tells out of text and nudges it toward your own writing style.
Pure Python 3, no dependencies.

Built from the 26 patterns in [blader/humanizer](https://github.com/blader/humanizer)
(which comes from Wikipedia's "Signs of AI writing").

## Use it

```
python -m humanizer draft.txt                 # rewritten text to stdout, score on stderr
python -m humanizer draft.txt -o clean.txt
cat draft.txt | python -m humanizer --seed 3
python -m humanizer --score draft.txt         # just list the AI tells found
```

## Your voice (already set up)

`samples/` holds your own writing, grouped by type: `academic/`, `essay/`, `speech/`, `personal/`.
The tool builds one style profile per folder and picks the closest one to each draft
(it prints which: `style: essay`). Override with `--register academic`.

It also keeps what is already yours: curly quotes, your dash style (` --- `, ` – ` or `—`),
your ellipsis style, British spelling, and any phrase from the AI-pattern list that you
genuinely use ("at the end of the day", "utilize"...). Run it on your own samples and 94–100%
of the words come back unchanged.

Only put text you wrote yourself in `samples/`. Anything AI-written will teach it the wrong habits.

## Teach it more

Drop your own writing (`.txt` / `.md`, 30+ words each, more is better) into `samples/`, then:

```
python -m humanizer --learn                   # prints + saves profile.json
python -m humanizer draft.txt                 # picks up samples/ automatically
```

The profile measures sentence length and spread, contraction rate, em dash and ellipsis use,
how often you start sentences with And/But/So, lowercase "i", and a few other habits.
The rewriter uses those numbers when it adds contractions, decides how many dashes to keep,
and splits or joins sentences. With no samples it falls back to a neutral default.

## What it fixes automatically

AI vocabulary (delve, pivotal, robust...), filler openers and closers ("In conclusion",
"It's important to note"), chatbot residue, "serves as" / "boasts", "not X, it's Y",
trailing `-ing` riders, em dash overuse, curly quotes, decorative bold and emoji headings,
and uniform sentence rhythm. Code fences are never touched.

## What it only flags

Vague attribution ("studies show") and forced triads need a real source or a human call.
`--score` lists them.

## Limits

This is rule-based, not a language model. It removes patterns; it can't make dull writing good,
and no tool can promise to beat a given AI detector. Read the output before you send it.

Tests: `python -m unittest discover -s tests -t .`

## Use it inside Claude chat

`skill/ayaahn-humanizer.zip` is a Claude Skill. In claude.ai: Settings > Capabilities > Skills > Upload skill,
pick the zip, switch it on. Then paste text in any chat and say "humanize this".
After adding new samples, rebuild the zip (see `skill/build.sh`).
