import argparse
import json
import sys
from pathlib import Path

from .detect import score
from .rewrite import humanize
from .style import analyze, build_profile, load_profile


def main(argv=None):
    ap = argparse.ArgumentParser(prog="humanizer", description="Strip AI tells and match your own writing style.")
    ap.add_argument("file", nargs="?", help="input file (default: stdin)")
    ap.add_argument("-o", "--out", help="write result here (default: stdout)")
    ap.add_argument("--samples", default="samples", help="folder of your own .txt/.md writing (default: ./samples)")
    ap.add_argument("--profile", help="saved profile JSON (overrides --samples)")
    ap.add_argument("--learn", action="store_true", help="analyze samples, save profile.json, and exit")
    ap.add_argument("--score", action="store_true", help="only print the AI-tell report")
    ap.add_argument("--seed", type=int, help="make output repeatable")
    ap.add_argument("--keep-bold", action="store_true")
    ap.add_argument("--no-rhythm", action="store_true", help="skip sentence splitting/merging")
    a = ap.parse_args(argv)

    if a.learn:
        prof = build_profile(a.samples)
        Path("profile.json").write_text(json.dumps(prof, indent=2))
        print(json.dumps(prof, indent=2))
        return 0

    text = Path(a.file).read_text(encoding="utf-8") if a.file else sys.stdin.read()
    if a.score:
        print(json.dumps(score(text), indent=2))
        return 0

    prof = load_profile(a.profile, a.samples)
    out = humanize(text, prof, seed=a.seed, strip_bold=not a.keep_bold, rhythm=not a.no_rhythm)
    before, after = score(text)["score"], score(out)["score"]
    sys.stderr.write(f"ai-tell score: {before} -> {after}  (style samples used: {prof['samples']})\n")
    if a.out:
        Path(a.out).write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)
    return 0
