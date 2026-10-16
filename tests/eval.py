"""Score every AI-written paragraph in tests/ai_corpus before and after the humanizer.
Run: python -m tests.eval        (prints a table; exit code 1 if any file ends above the limit)"""
import sys
from pathlib import Path

from humanizer import humanize, score
from humanizer.style import load_profile

LIMIT = 40                       # worst allowed score after humanizing; vague attribution needs a real source, so it stays
root = Path(__file__).resolve().parent.parent


def run():
    prof = load_profile(None, root / "samples")
    rows, worst = [], 0
    for f in sorted((root / "tests" / "ai_corpus").glob("*.txt")):
        t = f.read_text(encoding="utf-8")
        out = humanize(t, prof, seed=1)
        a, b = score(t), score(out)
        left = [x["category"] for x in b["findings"]]
        rows.append((f.stem, a["score"], b["score"], ", ".join(left) or "-"))
        worst = max(worst, b["score"])
    return rows, worst


if __name__ == "__main__":
    rows, worst = run()
    print(f"{'file':26}{'before':>7}{'after':>7}  left")
    for r in rows:
        print(f"{r[0]:26}{r[1]:>7}{r[2]:>7}  {r[3]}")
    sys.exit(1 if worst > LIMIT else 0)
