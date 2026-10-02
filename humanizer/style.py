"""Learn a writing-style profile from the user's own text samples."""
import json
import re
import statistics
from pathlib import Path

from .textutil import sentences, words

# Used when no samples exist. Mildly formal, uneven rhythm, few dashes.
DEFAULT_PROFILE = {
    "samples": 0,
    "mean_sentence_len": 18.0,
    "sentence_len_stdev": 9.0,
    "contractions_per_100w": 1.2,
    "em_dashes_per_100w": 0.15,
    "ellipses_per_100w": 0.0,
    "semicolons_per_100w": 0.1,
    "conjunction_start_rate": 0.05,
    "question_rate": 0.03,
    "exclamation_rate": 0.0,
    "lowercase_i_rate": 0.0,
    "lowercase_start_rate": 0.0,
    "commas_per_sentence": 1.6,
    "first_person_per_100w": 1.0,
}

_CONJ = {"and", "but", "so", "or", "because", "yet"}
_CONTR = re.compile(r"\b\w+['’](?:t|s|re|ve|ll|d|m)\b", re.I)


def analyze(text):
    """Return a style profile dict for a block of text."""
    sents = [s for s in sentences(text) if len(words(s)) > 0]
    w = words(text)
    n = max(len(w), 1)
    lens = [len(words(s)) for s in sents] or [0]
    per100 = lambda c: round(100 * c / n, 3)
    first_chars = [s.lstrip("\"'([")[:1] for s in sents if s.lstrip("\"'([")]
    lower_starts = sum(1 for c in first_chars if c.isalpha() and c.islower())
    return {
        "samples": 1,
        "words": len(w),
        "mean_sentence_len": round(statistics.mean(lens), 2),
        "sentence_len_stdev": round(statistics.pstdev(lens), 2),
        "contractions_per_100w": per100(len(_CONTR.findall(text))),
        "em_dashes_per_100w": per100(text.count("—") + len(re.findall(r"\s--\s", text))),
        "ellipses_per_100w": per100(len(re.findall(r"\.{3}|…", text))),
        "semicolons_per_100w": per100(text.count(";")),
        "conjunction_start_rate": round(
            sum(1 for s in sents if words(s) and words(s)[0].lower() in _CONJ) / max(len(sents), 1), 3),
        "question_rate": round(sum(1 for s in sents if s.endswith("?")) / max(len(sents), 1), 3),
        "exclamation_rate": round(sum(1 for s in sents if s.endswith("!")) / max(len(sents), 1), 3),
        "lowercase_i_rate": round(len(re.findall(r"\bi\b", text)) /
                                  max(len(re.findall(r"\b[iI]\b", text)), 1), 3),
        "lowercase_start_rate": round(lower_starts / max(len(first_chars), 1), 3),
        "commas_per_sentence": round(text.count(",") / max(len(sents), 1), 2),
        "first_person_per_100w": per100(len(re.findall(r"\b(?:I|my|me|we|our)\b", text, re.I))),
        "top_openers": _top([words(s)[0].lower() for s in sents if words(s)], 8),
        "top_words": _top([x.lower() for x in w if len(x) > 4], 15),
    }


def _top(items, k):
    counts = {}
    for i in items:
        counts[i] = counts.get(i, 0) + 1
    return [x for x, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:k]]


def build_profile(samples_dir):
    """Merge per-file profiles, weighted by word count."""
    files = sorted(p for p in Path(samples_dir).glob("**/*") if p.suffix.lower() in {".txt", ".md"})
    profs = []
    for f in files:
        t = f.read_text(encoding="utf-8", errors="ignore")
        if len(words(t)) >= 30:
            profs.append(analyze(t))
    if not profs:
        return dict(DEFAULT_PROFILE)
    total = sum(p["words"] for p in profs)
    merged = {"samples": len(profs), "words": total}
    for k in DEFAULT_PROFILE:
        if k == "samples":
            continue
        merged[k] = round(sum(p[k] * p["words"] for p in profs) / total, 3)
    merged["top_openers"] = _top([o for p in profs for o in p["top_openers"]], 8)
    merged["top_words"] = _top([o for p in profs for o in p["top_words"]], 15)
    return merged


def load_profile(path=None, samples_dir=None):
    if path and Path(path).exists():
        return {**DEFAULT_PROFILE, **json.loads(Path(path).read_text())}
    if samples_dir and Path(samples_dir).exists():
        return build_profile(samples_dir)
    return dict(DEFAULT_PROFILE)
