"""Learn writing-style profiles from the user's own text samples.

Samples live in samples/<register>/*.txt (e.g. academic, essay, speech, personal).
Each register gets its own profile, and one merged profile covers everything."""
import json
import re
import statistics
from pathlib import Path

from . import patterns as P
from .textutil import sentences, words

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
    "curly_quote_rate": 0.5,          # 0.5 = unknown: leave quotes alone
    "dash_token": " — ",
    "ellipsis_token": "...",
    "own_phrases": [],                # AI-flagged words/phrases the user really writes
}

_CONJ = {"and", "but", "so", "or", "because", "yet"}
_CONTR = re.compile(r"\b(?:\w+n['’]t|(?:it|that|there|he|she|what|let|who|here)['’]s|\w+['’](?:re|ve|ll|d|m))\b", re.I)
_NUMERIC = [k for k, v in DEFAULT_PROFILE.items() if isinstance(v, (int, float)) and k != "samples"]
_FEATURES = [("mean_sentence_len", 10), ("contractions_per_100w", 1.5),
             ("first_person_per_100w", 3), ("commas_per_sentence", 1.5)]


def _own_phrases(text):
    low = text.lower()
    found = set()
    for pat, _ in P.PHRASES:
        for m in re.finditer(r"\b" + pat if pat[0] not in "(\\" or pat.startswith("(?") else pat, low):
            found.add(m.group(0).strip(" ,"))
    for w in P.WORDS:
        if re.search(rf"\b{re.escape(w)}\b", low):
            found.add(w)
    return sorted(f for f in found if f)


def analyze(text):
    sents = [s for s in sentences(text) if words(s)]
    w = words(text)
    n = max(len(w), 1)
    lens = [len(words(s)) for s in sents] or [0]
    per100 = lambda c: round(100 * c / n, 3)
    first = [s.lstrip("\"'([“‘")[:1] for s in sents if s.lstrip("\"'([“‘")]
    curly = len(re.findall("[“”‘’]", text))
    straight = len(re.findall(r"[\"']", text))
    dashes = {" --- ": len(re.findall(r"\s---\s", text)), " – ": len(re.findall(r"\s–\s", text)),
              " — ": len(re.findall(r"\s?—\s?", text)), " - ": len(re.findall(r"\s-\s{1,2}\S", text))}
    ell = {"…": text.count("…"), "...": len(re.findall(r"\.{3}", text)), ". . .": text.count(". . .")}
    return {
        "samples": 1, "words": len(w),
        "mean_sentence_len": round(statistics.mean(lens), 2),
        "sentence_len_stdev": round(statistics.pstdev(lens), 2),
        "contractions_per_100w": per100(len(_CONTR.findall(text))),
        "em_dashes_per_100w": per100(sum(dashes.values())),
        "ellipses_per_100w": per100(sum(ell.values())),
        "semicolons_per_100w": per100(text.count(";")),
        "conjunction_start_rate": round(sum(1 for s in sents if words(s)[0].lower() in _CONJ) / max(len(sents), 1), 3),
        "question_rate": round(sum(1 for s in sents if s.endswith("?")) / max(len(sents), 1), 3),
        "exclamation_rate": round(sum(1 for s in sents if s.endswith("!")) / max(len(sents), 1), 3),
        "lowercase_i_rate": round(len(re.findall(r"\bi\b", text)) / max(len(re.findall(r"\b[iI]\b", text)), 1), 3),
        "lowercase_start_rate": round(sum(1 for c in first if c.isalpha() and c.islower()) / max(len(first), 1), 3),
        "commas_per_sentence": round(text.count(",") / max(len(sents), 1), 2),
        "first_person_per_100w": per100(len(re.findall(r"\b(?:I|my|me|we|our)\b", text, re.I))),
        "curly_quote_rate": round(curly / (curly + straight), 3) if curly + straight else 0.5,
        "dash_token": max(dashes, key=dashes.get) if any(dashes.values()) else " — ",
        "ellipsis_token": max(ell, key=ell.get) if any(ell.values()) else "...",
        "own_phrases": _own_phrases(text),
        "top_openers": _top([words(s)[0].lower() for s in sents], 8),
        "top_words": _top([x.lower() for x in w if len(x) > 4], 15),
    }


def _top(items, k):
    counts = {}
    for i in items:
        counts[i] = counts.get(i, 0) + 1
    return [x for x, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:k]]


def _merge(profs):
    total = sum(p["words"] for p in profs)
    m = {"samples": len(profs), "words": total}
    for k in _NUMERIC:
        m[k] = round(sum(p[k] * p["words"] for p in profs) / total, 3)
    for k in ("dash_token", "ellipsis_token"):
        m[k] = _top([p[k] for p in profs], 1)[0]
    m["own_phrases"] = sorted({x for p in profs for x in p["own_phrases"]})
    m["top_openers"] = _top([o for p in profs for o in p["top_openers"]], 8)
    m["top_words"] = _top([o for p in profs for o in p["top_words"]], 15)
    return m


def build_profile(samples_dir):
    """Merged profile plus one per sub-folder ("register")."""
    root = Path(samples_dir)
    by_reg = {}
    for f in sorted(p for p in root.glob("**/*") if p.suffix.lower() in {".txt", ".md"} and p.name.lower() != "readme.md"):
        t = f.read_text(encoding="utf-8", errors="ignore")
        if len(words(t)) >= 30:
            reg = f.parent.name if f.parent != root else "general"
            by_reg.setdefault(reg, []).append(analyze(t))
    if not by_reg:
        return dict(DEFAULT_PROFILE)
    merged = _merge([p for ps in by_reg.values() for p in ps])
    merged["registers"] = {r: _merge(ps) for r, ps in by_reg.items()}
    return merged


def pick_register(profile, text):
    """Choose the register whose style is closest to the draft being rewritten."""
    regs = profile.get("registers")
    if not regs or len(words(text)) < 20:
        return profile
    d = analyze(text)
    def dist(p):
        return sum(((d[k] - p[k]) / s) ** 2 for k, s in _FEATURES)
    name = min(regs, key=lambda r: dist(regs[r]))
    return {**profile, **regs[name], "register": name}


def load_profile(path=None, samples_dir=None):
    if path and Path(path).exists():
        return {**DEFAULT_PROFILE, **json.loads(Path(path).read_text())}
    if samples_dir and Path(samples_dir).exists():
        return {**DEFAULT_PROFILE, **build_profile(samples_dir)}
    return dict(DEFAULT_PROFILE)
