"""Usage: python run.py input.txt [--register academic|essay|speech|personal] [--score]
Prints the humanized text to stdout and a short report to stderr."""
import argparse, json, sys
from pathlib import Path

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
from humanizer import humanize, score
from humanizer.style import load_profile, pick_register

ap = argparse.ArgumentParser()
ap.add_argument("file", nargs="?")
ap.add_argument("--register", default="auto")
ap.add_argument("--score", action="store_true")
ap.add_argument("--seed", type=int)
a = ap.parse_args()

text = Path(a.file).read_text(encoding="utf-8") if a.file else sys.stdin.read()
if a.score:
    print(json.dumps(score(text), indent=2))
    sys.exit(0)
prof = load_profile(here / "profile.json", here.parent.parent.parent / "samples")
if not prof["samples"]:
    sys.stderr.write("warning: profile.json missing, so no style rules were applied (quotes, dashes, register). "
                     "Rebuild the skill with skill/build.sh.\n")
reg = pick_register(prof, text).get("register", "none") if a.register == "auto" else a.register
out = humanize(text, prof, seed=a.seed, register=a.register)
left = score(out)["findings"]
flags = [f"{f['category']} x{f['count']}" for f in left
         if f["category"] in {"vague-attribution", "triads", "ai-vocabulary", "stock-phrases"}]
sys.stderr.write(f"style: {reg} | ai-tell score {score(text)['score']} -> {score(out)['score']}"
                 + (f" | still flagged: {', '.join(flags)}" if flags else "") + "\n")
for f in left:                                   # exact wording the script left for you to fix by hand
    if f.get("examples"):
        sys.stderr.write(f"  left: {f['category']}: " + " | ".join(f["examples"]) + "\n")
b = score(out)["burstiness"]
if b is not None and b < 0.45:
    sys.stderr.write(f"  rhythm: sentence lengths are even (burstiness {b}); vary a few by hand, without adding words\n")
sys.stdout.write(out)
