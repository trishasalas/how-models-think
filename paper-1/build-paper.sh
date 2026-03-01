#!/bin/bash

# build-paper.sh
# Run from paper-1/ directory
# Requires: pandoc, lualatex (MacTeX)
#   brew install pandoc
#   brew install --cask mactex
#
# Produces a tagged PDF/UA-2 + PDF/A-4f document via the template in
# paper/template.tex, which enables \DocumentMetadata tagging. This
# requires a TeX Live 2022+ / MacTeX 2022+ installation.
#
# Accessibility checklist before building:
#   - All figures referenced with descriptive alt text: ![Describe what a
#     sighted reader sees](../figures/filename.png)
#   - paper/metadata.yaml has: title, author, date, abstract, lang
#   - paper/sections/10-colophon.md is written

set -e

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
  "$SECTIONS/09-references.md" \
  "$SECTIONS/10-colophon.md" \
  -o "$OUTPUT" \
  --pdf-engine=lualatex \
  --template=paper/template.tex \
  --wrap=none \
  --citeproc \
  -V documentclass=extarticle \
  -V geometry:margin=1in \
  -V mainfont="Atkinson Hyperlegible" \
  -V fontsize=12pt \
  -V linestretch=1.15 \
  -V colorlinks=true

echo "Done: $OUTPUT"
