#!/bin/bash

# build-paper.sh
# Run from paper-1-emergence/ directory
# Requires: pandoc, and a LaTeX engine (e.g. BasicTeX or MacTeX)
# Install pandoc: brew install pandoc
# Install BasicTeX: brew install --cask basictex

OUTPUT="accessibility-emergence-paper.pdf"
SECTIONS="paper/sections"

pandoc \
  "$SECTIONS/01-abstract.md" \
  "$SECTIONS/02-introduction.md" \
  "$SECTIONS/03-related.md" \
  "$SECTIONS/04-methodology.md" \
  "$SECTIONS/05-results.md" \
  "$SECTIONS/06-discussion.md" \
  "$SECTIONS/07-conclusion.md" \
  -o "$OUTPUT" \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=16pt \
  -V linestretch=1.5 \
  -V colorlinks=true \
  --toc \
  --toc-depth=2

echo "Done: $OUTPUT"
