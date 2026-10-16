"""Score text for AI tells. 0 = reads human, 100 = textbook AI."""
import re
import statistics

from . import patterns as P
from .textutil import sentences, words


_LEAK_RX = [re.compile(r"(?:cite|i|navlist)?(?:turn\d+(?:search|news|file|image|view)\d+)+"),
            re.compile(r"contentReference\[oaicite|oai_citation|<\|endoftext\|>"),
            re.compile(r"utm_source=(?:chatgpt\.com|openai)")]
_HEDGE = re.compile(r"\b(?:could|might|may|can) (?:potentially|possibly|conceivably|arguably)\b", re.I)
_EMOJI = "\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B55"
_SMALL = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "the", "to", "with", "vs"}


def _title_case(h):
    ws = [w for w in re.findall(r"[A-Za-z][A-Za-z'’-]*", h)]
    main = [w for w in ws[1:] if w.lower() not in _SMALL]
    return len(ws) >= 4 and len(main) >= 3 and all(w[0].isupper() for w in main)


def _repeated_openers(text):
    firsts = [words(s)[0].lower() for s in sentences(text) if words(s)]
    runs, n = 0, 1
    for a, b in zip(firsts, firsts[1:]):
        n = n + 1 if a == b else 1
        if n == 3:
            runs += 1
    return runs


def findings(text):
    out = []
    low = text.lower()

    def add(cat, n, note, ex=()):
        if n:
            item = {"category": cat, "count": n, "note": note}
            if ex:
                item["examples"] = list(dict.fromkeys(ex))[:4]
            out.append(item)

    def hit(rx, src, flags=0):
        """Count and sample the matched wording so a reviewer knows what to fix."""
        found = [re.sub(r"\s+", " ", m.group(0)).strip() for m in re.finditer(rx, src, flags)]
        return len(found), found

    ai_words = sum(len(re.findall(rf"\b{re.escape(w)}\b", low)) for w in P.WORDS
                   if w not in {"numerous", "many", "unlock"})
    add("ai-vocabulary", ai_words, "words like delve, pivotal, crucial, robust, leverage")
    add("stock-phrases", sum(len(re.findall(p, low)) for p, _ in P.PHRASES[:30]),
        "filler openers, chatbot residue, summary closers")
    add("stock-phrases", sum(len(re.findall(p, low)) for p, rep in P.TELL_PHRASES if rep == "" or rep.endswith(", ")),
        "run-ups, flattery, closers like 'Read that again'")
    add("markup-leak", sum(len(rx.findall(text)) for rx in _LEAK_RX),
        "chatbot citation markup or tracking parameters left in the text (near-certain)")
    n, ex = hit(_HEDGE, text)
    add("hedge-stack", n, "'could potentially', 'might possibly'", ex)
    for cat, pat, note, _ in P.FLAG_ONLY:
        n, ex = hit(pat, low if cat != "placeholder" else text, re.I)
        add(cat, n, note + " (needs a human call)", ex)
    add("title-case-headings", sum(1 for h in re.findall(r"^#{1,6} +(.+)$", text, re.M) if _title_case(h)),
        "every main word capitalised; sentence case reads more human (proper nouns need a human call)")
    add("inline-header-lists", len(re.findall(r"^\s*(?:[-*+]|\d+[.)]) +\*\*[^*\n]+:?\*\*:?", text, re.M)),
        "bullets that each start with a bold label")
    n, ex = hit(r"\bfrom [^.;]{3,60}? to [^.;]{3,60}?,? from [^.;]{3,60}? to\b", low)
    add("false-range", n, "'from X to Y, from A to B' with no real scale", ex)
    add("repeated-openers", _repeated_openers(text), "three or more sentences in a row starting with the same word")
    add("emoji-lines", len(re.findall(rf"^[ \t]*(?:[-*+]|\d+[.)])?[ \t]*[{_EMOJI}]", text, re.M)),
        "emoji leading lines or bullets")
    n2, ex2 = hit(r"\b(?:is|are|was|were)(?: not|n(?:'|’)t) (?:just|only|merely|simply) [^.;!?]{2,60}?[;,—-]+ ?(?:it(?:'|’)s|it is|this is|that is)\b", low)
    add("negative-parallelism", n2, "'X is not merely Y; it is Z' framing", ex2)
    add("negative-parallelism",
        len(re.findall(r"\b(?:it|this|that)(?:(?:'|’)s| is| was)? ?(?:not|n(?:'|’)t) (?:just |only |merely |simply )?(?!that\b)"
                       r"[^.;!?]{2,60}?[,;—-]+ ?(?:but|it(?:'|’)s|it is|this is)\b", low)),
        "'not X, it's Y' framing")
    tails = "|".join(P.TAIL_VERBS + P.TAIL_VERBS_FLAG_ONLY)
    add("ing-tail", len(re.findall(rf",\s+(?:{tails})\b", low)), "vague -ing clause tacked on a sentence")
    n, ex = hit(P.VAGUE_ATTRIBUTION, low)
    add("vague-attribution", n, "needs a named source (cannot be fixed automatically)", ex)
    add("em-dashes", max(text.count("—") - 1, 0), "em dashes beyond the first")
    add("bold", len(re.findall(r"\*\*[^*]+\*\*", text)), "decorative bold")
    add("emoji-headings", len(re.findall(r"^#+ .*[\U0001F300-\U0001FAFF☀-➿]", text, re.M)),
        "emoji in headings")
    # lowercase items only: "Instagram, X, and TikTok" is a real list of names, not a rhetorical triad
    n, ex = hit(r"\b[a-z][\w-]*, [a-z][\w-]*,? and [a-z][\w-]*\b", text)
    add("triads", n, "possible forced list of three", ex)
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
               "emoji-headings": 4, "triads": 3,
               "markup-leak": 15, "hedge-stack": 4, "title-case-headings": 2,
               "inline-header-lists": 3, "false-range": 4, "repeated-openers": 3,
               "emoji-lines": 3, **{c: w for c, _, _, w in P.FLAG_ONLY}}
    raw = sum(weights[x["category"]] * x["count"] for x in f)
    s = min(100.0, raw * 100 / n * 2.2)
    b = burstiness(text)
    if b is not None and b < 0.45:                 # metronomic rhythm
        s = min(100.0, s + (0.45 - b) * 40)
    return {"score": round(s), "burstiness": b, "findings": f}
