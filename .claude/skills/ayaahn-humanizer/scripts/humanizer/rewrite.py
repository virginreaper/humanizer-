"""Rewrite engine. Mechanical AI-pattern removal first, then style passes
driven by the user's profile so the output drifts toward their own voice."""
import random
import re

from . import patterns as P
from .style import DEFAULT_PROFILE
from .textutil import (is_prose_paragraph, match_case, recapitalize, sentences,
                       split_fences, words)

_SUBJECT_STARTS = {"the", "it", "this", "that", "he", "she", "they", "we", "there",
                   "these", "those", "a", "an", "its", "their", "some", "most", "many"}


def _phrases(t, own):
    for pat, rep in P.PHRASES:
        t = re.sub(r"\b" + pat if pat[0] not in "(\\" or pat.startswith("(?") else pat,
                   lambda m, r=rep: m.group(0) if m.group(0).lower().strip(" ,") in own else match_case(m.group(0), r),
                   t, flags=re.I)
    return t


def _vocab(t, own):
    def landscape(m):
        return match_case(m.group(1), m.group(1)) + (" scene" if m.group(1).lower() in P.LANDSCAPE_CTX else " landscape")
    t = re.sub(P.LANDSCAPE, landscape, t, flags=re.I)
    pat = r"\b(" + "|".join(sorted(map(re.escape, P.WORDS), key=len, reverse=True)) + r")\b"
    return re.sub(pat, lambda m: m.group(1) if m.group(1).lower() in own
                  else match_case(m.group(1), P.WORDS[m.group(1).lower()]), t, flags=re.I)


def _structure(t):
    # "It's not just X, it's Y." -> "It's Y."
    t = re.sub(r"\b(?:it|this|that)(?:'|’)?s? (?:is )?not (?:just |only |merely |simply )?(?:about )?[^.;!?]{2,80}?[,;—-]+\s*(?:but |it(?:'|’)s |it is |this is )(?:also |about )?",
               lambda m: "It is ", t, flags=re.I)
    # trailing "-ing" riders: ", highlighting how ..." -> "."
    tails = "|".join(map(re.escape, P.TAIL_VERBS))
    t = re.sub(rf"(?:,|\s—|\s--)\s+(?:{tails})\b[^.!?]*([.!?])", r"\1", t, flags=re.I)
    return t


def _typography(t, profile, strip_bold=True):
    if profile["curly_quote_rate"] < 0.05:
        t = t.translate({0x201C: '"', 0x201D: '"', 0x2018: "'", 0x2019: "'"})
    if strip_bold:
        t = re.sub(r"\*\*([^*\n]+)\*\*", r"\1", t)
    t = re.sub(r"^(#+ )[^\w\n]*", r"\1", t, flags=re.M)       # emoji/arrows in headings
    return t


def _dashes(t, profile, rng):
    n_words = max(len(words(t)), 1)
    budget = round(profile["em_dashes_per_100w"] * n_words / 100)
    ell = profile["ellipses_per_100w"] > 0.15
    dashes = list(re.finditer(r"\s*—\s*", t))
    token, ell_tok = profile["dash_token"], profile["ellipsis_token"]
    keep = set(rng.sample(range(len(dashes)), min(budget, len(dashes)))) if dashes else set()
    out, last = [], 0
    for i, m in enumerate(dashes):
        out.append(t[last:m.start()])
        if i in keep:
            out.append(token)
        elif ell and rng.random() < min(profile["ellipses_per_100w"] / 0.5, 0.6):
            out.append(ell_tok + " ")
        else:
            out.append(", ")
        last = m.end()
    out.append(t[last:])
    return "".join(out)


def _contractions(t, profile, rng):
    p = min(profile["contractions_per_100w"] / 2.0, 1.0)      # ~2/100w => always
    curly = profile["curly_quote_rate"] > 0.5
    for pat, rep in P.CONTRACTIONS:
        rep = rep.replace("'", "’") if curly else rep
        if "n't" not in rep:                 # "here we are." must not become "here we're."
            pat += r"(?=\s+[A-Za-z])"
        t = re.sub(pat, lambda m, r=rep: match_case(m.group(0), r) if rng.random() < p else m.group(0),
                   t, flags=re.I if pat[0] != r"\bI" else 0)
    return t


def _rhythm(par, profile, rng):
    """Push sentence lengths toward the profile's spread: split run-ons,
    glue neighbouring fragments, now and then start with And/But/So."""
    sents = sentences(par)
    if len(sents) < 2:
        return par
    target_mean, target_sd = profile["mean_sentence_len"], profile["sentence_len_stdev"]
    out, i = [], 0
    while i < len(sents):
        s = sents[i]
        n = len(words(s))
        if n > max(target_mean + 1.6 * target_sd, 30):
            m = re.search(r",\s+(but|and|so|yet)\s+", s[len(s)//3: 2*len(s)//3 + 20])
            if m:
                cut = len(s)//3 + m.start()
                head, conj, rest = s[:cut], m.group(1), s[len(s)//3 + m.end():]
                if rng.random() < max(profile["conjunction_start_rate"] * 6, 0.4) and words(rest):
                    out.append(head + ".")
                    out.append(conj.capitalize() + " " + rest)
                    i += 1
                    continue
        if (i + 1 < len(sents) and n < 8 and len(words(sents[i + 1])) < 9
                and target_sd < 6 and s[-1] == "." and rng.random() < 0.5):
            nxt = sents[i + 1]
            first = words(nxt)[0].lower() if words(nxt) else ""
            if first in _SUBJECT_STARTS:
                out.append(s[:-1] + ", and " + nxt[0].lower() + nxt[1:])
                i += 2
                continue
        out.append(s)
        i += 1
    return " ".join(out)


def _casual(t, profile):
    if profile["lowercase_i_rate"] > 0.6:
        t = re.sub(r"\bI\b", "i", t)
        t = re.sub(r"\bI(?=['’])", "i", t)
    return t


def humanize(text, profile=None, seed=None, strip_bold=True, rhythm=True, register="auto"):
    from .style import pick_register
    profile = {**DEFAULT_PROFILE, **(profile or {})}
    if register == "auto":
        profile = pick_register(profile, text)
    elif register in profile.get("registers", {}):
        profile = {**profile, **profile["registers"][register], "register": register}
    own = set(profile["own_phrases"])
    rng = random.Random(seed)
    result = []
    for is_code, chunk in split_fences(text):
        if is_code:
            result.append(chunk)
            continue
        t = _typography(chunk, profile, strip_bold)
        t = _phrases(t, own)
        t = _structure(t)
        t = _vocab(t, own)
        t = _dashes(t, profile, rng)
        t = _contractions(t, profile, rng)
        pars = re.split(r"(\n\s*\n)", t)
        pars = [(_rhythm(p, profile, rng) if rhythm and is_prose_paragraph(p) else p) for p in pars]
        t = "".join(pars)
        t = re.sub(r"[ \t]{2,}", " ", t)
        t = re.sub(r" +([,.;:!?])", r"\1", t)
        t = re.sub(r",\s*,", ",", t)
        t = recapitalize(t)
        if profile["lowercase_start_rate"] > 0.6:
            t = re.sub(r"(^|(?<=[.!?]) )([A-Z])(?=[a-z])", lambda m: m.group(1) + m.group(2).lower(), t, flags=re.M)
        t = _casual(t, profile)
        if profile["curly_quote_rate"] > 0.5:
            t = re.sub(r"(?<=\w)'(?=\w)", "’", t)
        result.append(t)
    return "".join(result).strip() + "\n"
