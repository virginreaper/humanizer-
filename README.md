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

## Teach it your voice

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
