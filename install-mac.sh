#!/bin/bash
# Installs the reel-edit-style Claude Code skill and everything it needs on macOS.
# Safe to run again: it skips what is already installed.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills/reel-edit-style"
echo "== 1/5 Homebrew"
if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is missing. Installing it (it may ask for your Mac password)..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  [ -x /opt/homebrew/bin/brew ] && eval "$(/opt/homebrew/bin/brew shellenv)"
  [ -x /usr/local/bin/brew ] && eval "$(/usr/local/bin/brew shellenv)"
fi
echo "== 2/5 Tools: python, ffmpeg, node, whisper-cpp, yt-dlp"
for p in python ffmpeg node whisper-cpp yt-dlp; do
  if brew list --formula "$p" >/dev/null 2>&1; then echo "  $p already installed"; else brew install "$p"; fi
done
echo "== 3/5 Whisper speech model (~550 MB, once)"
MODEL="$HOME/.whisper-models/ggml-large-v3-turbo-q5_0.bin"
if [ -f "$MODEL" ]; then echo "  model already present"; else
  mkdir -p "$HOME/.whisper-models"
  curl -L --fail -o "$MODEL.part" "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin" && mv "$MODEL.part" "$MODEL"
fi
echo "== 4/5 Skill -> $DEST"
mkdir -p "$HOME/.claude/skills"
rm -rf "$DEST"; cp -R "$HERE/skill/reel-edit-style" "$DEST"
echo "== 5/5 Hyperframes renderer (downloads itself once) + final check"
npx --yes hyperframes@0.9.7 --version >/dev/null 2>&1 || true
python3 "$DEST/scripts/check_setup.py"
echo
echo "Done. Restart Claude Code, then say: \"Make a reel from <file> using the reel-edit-style skill\"."
