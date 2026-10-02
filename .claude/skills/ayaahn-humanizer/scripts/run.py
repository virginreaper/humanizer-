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
prof = load_profile(here / "profile.json")
reg = pick_register(prof, text).get("register", "none") if a.register == "auto" else a.register
out = humanize(text, prof, seed=a.seed, register=a.register)
flags = [f"{f['category']} x{f['count']}" for f in score(out)["findings"]
         if f["category"] in {"vague-attribution", "triads", "ai-vocabulary", "stock-phrases"}]
sys.stderr.write(f"style: {reg} | ai-tell score {score(text)['score']} -> {score(out)['score']}"
                 + (f" | still flagged: {', '.join(flags)}" if flags else "") + "\n")
sys.stdout.write(out)
