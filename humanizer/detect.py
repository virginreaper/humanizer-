"""Score text for AI tells. 0 = reads human, 100 = textbook AI."""
import re
import statistics

from . import patterns as P
from .textutil import sentences, words


def findings(text):
    out = []
    low = text.lower()

    def add(cat, n, note):
        if n:
            out.append({"category": cat, "count": n, "note": note})

    ai_words = sum(len(re.findall(rf"\b{re.escape(w)}\b", low)) for w in P.WORDS
                   if w not in {"numerous", "many", "unlock"})
    add("ai-vocabulary", ai_words, "words like delve, pivotal, crucial, robust, leverage")
    add("stock-phrases", sum(len(re.findall(p, low)) for p, _ in P.PHRASES[:30]),
        "filler openers, chatbot residue, summary closers")
    add("negative-parallelism",
        len(re.findall(r"\bnot (?:just |only |merely |simply )?[^.;!?]{2,60}?[,;—-]+ ?(?:but|it(?:'|’)s|it is)\b", low)),
        "'not X, it's Y' framing")
    tails = "|".join(P.TAIL_VERBS)
    add("ing-tail", len(re.findall(rf",\s+(?:{tails})\b", low)), "vague -ing clause tacked on a sentence")
    add("vague-attribution", len(re.findall(P.VAGUE_ATTRIBUTION, low)),
        "needs a named source (cannot be fixed automatically)")
    add("em-dashes", max(text.count("—") - 1, 0), "em dashes beyond the first")
    add("bold", len(re.findall(r"\*\*[^*]+\*\*", text)), "decorative bold")
    add("curly-quotes", len(re.findall("[“”‘’]", text)), "curly quotes")
    add("emoji-headings", len(re.findall(r"^#+ .*[\U0001F300-\U0001FAFF☀-➿]", text, re.M)),
        "emoji in headings")
    add("triads", len(re.findall(r"\b[\w-]+, [\w-]+,? and [\w-]+\b", low)),
        "possible forced list of three")
    return out


def burstiness(text):
    lens = [len(words(s)) for s in sentences(text) if words(s)]
    if len(lens) < 3:
        return None
    return round(statistics.pstdev(lens) / max(statistics.mean(lens), 1), 3)


def score(text):
    f = findings(text)
    n = max(len(words(text)), 1)
    weights = {"ai-vocabulary": 6, "stock-phrases": 8, "negative-parallelism": 10,
               "ing-tail": 7, "vague-attribution": 6, "em-dashes": 3, "bold": 2,
               "curly-quotes": 1, "emoji-headings": 4, "triads": 3}
    raw = sum(weights[x["category"]] * x["count"] for x in f)
    s = min(100.0, raw * 100 / n * 2.2)
    b = burstiness(text)
    if b is not None and b < 0.45:                 # metronomic rhythm
        s = min(100.0, s + (0.45 - b) * 40)
    return {"score": round(s), "burstiness": b, "findings": f}
