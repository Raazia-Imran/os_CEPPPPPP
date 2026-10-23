$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
& pdflatex -interaction=nonstopmode -halt-on-error main.tex
if ($LASTEXITCODE -ne 0) { throw "First LaTeX pass failed" }
& bibtex main
if ($LASTEXITCODE -ne 0) { throw "BibTeX failed" }
1..2 | ForEach-Object {
  & pdflatex -interaction=nonstopmode -halt-on-error main.tex
  if ($LASTEXITCODE -ne 0) { throw "LaTeX pass failed" }
}
