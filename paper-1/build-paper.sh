#!/bin/bash

# build-paper.sh
# Run from paper-1-emergence/ directory
# Requires: pandoc, lualatex (MacTeX or BasicTeX)
# Install pandoc: brew install pandoc
# Install MacTeX: brew install --cask mactex

OUTPUT="accessibility-emergence-paper.pdf"
SECTIONS="paper/sections"

pandoc \
--metadata-file=paper/metadata.yaml \
  "$SECTIONS/02-introduction.md" \
  "$SECTIONS/03-related.md" \
  "$SECTIONS/04-methodology.md" \
  "$SECTIONS/05-results.md" \
  "$SECTIONS/06-discussion.md" \
  "$SECTIONS/07-conclusion.md" \
  "$SECTIONS/08-limitations.md" \
  -o "$OUTPUT" \
  --pdf-engine=lualatex \
  --template=paper/template.tex \
  --wrap=none \
  --citeproc \
  -V documentclass=article \
  -V geometry:margin=1in \
  -V mainfont="Atkinson Hyperlegible" \
  -V fontsize=11pt \
  -V linestretch=1.5 \
  -V colorlinks=true

echo "Done: $OUTPUT"
