"""Small shared helpers: sentence splitting, word counting, code-fence handling."""
import re

ABBREV = {"e.g.", "i.e.", "vs.", "etc.", "mr.", "mrs.", "ms.", "dr.", "prof.",
          "no.", "fig.", "st.", "inc.", "ltd.", "u.s.", "cf.", "v."}

_SPLIT = re.compile(r'(?<=[.!?])["\')\]]*\s+(?=["\'(\[]*[A-Za-z0-9])')
_FENCE = re.compile(r"(```.*?```)", re.S)


def words(text):
    return re.findall(r"[A-Za-z0-9]+(?:['’][A-Za-z]+)?", text)


def sentences(text):
    """Split prose into sentences, not breaking on common abbreviations."""
    parts, start = [], 0
    for m in _SPLIT.finditer(text):
        chunk = text[start:m.start() + 1]
        last = chunk.split()[-1].lower() if chunk.split() else ""
        if last in ABBREV:
            continue
        parts.append(text[start:m.end()].strip())
        start = m.end()
    tail = text[start:].strip()
    if tail:
        parts.append(tail)
    return parts


def split_fences(text):
    """Yield (is_code, chunk) so code blocks are never rewritten."""
    for chunk in _FENCE.split(text):
        if chunk:
            yield chunk.startswith("```"), chunk


def is_prose_paragraph(p):
    s = p.lstrip()
    return bool(s) and not re.match(r"(#|[-*+] |\d+[.)] |>|\||    )", s)


def match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def recapitalize(text):
    """Capitalize sentence starts (after removals), skipping abbreviations."""
    def fix(m):
        before = text[:m.start()].split()
        if before and before[-1].lower() in ABBREV:
            return m.group(0)
        return m.group(1) + m.group(2).upper()
    text = re.sub(r"(^|\n\s*|(?<=[.!?])[\"')\]]*\s+)([a-z])", fix, text)
    return text
