pandoc \
  paper/sections/01-abstract.md \
  --pdf-engine=lualatex \
  --template=paper/template.tex \
  -V documentclass=extarticle \
  -s \
  -o /tmp/test-output.tex && head -30 /tmp/test-output.tex