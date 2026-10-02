#!/bin/sh
# Rebuild the Claude skill zip from the current code and samples/.
set -e
cd "$(dirname "$0")/.."
python3 -m humanizer --learn >/dev/null
cp profile.json skill/ayaahn-humanizer/scripts/profile.json && rm profile.json
rm -rf skill/ayaahn-humanizer/scripts/humanizer && cp -r humanizer skill/ayaahn-humanizer/scripts/humanizer
find skill -name __pycache__ -prune -exec rm -rf {} +
cd skill && rm -f ayaahn-humanizer.zip && zip -qr ayaahn-humanizer.zip ayaahn-humanizer
# keep the Claude Code copy (/ayaahn-humanizer) in sync
rm -rf ../.claude/skills/ayaahn-humanizer && mkdir -p ../.claude/skills && cp -r ayaahn-humanizer ../.claude/skills/
