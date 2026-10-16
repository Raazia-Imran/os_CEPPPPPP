# Build the current report

Run in this folder:

```sh
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Required packages are standard TeX Live packages:geometry,lmodern,microtype,booktabs,longtable,array,graphicx,enumitem,xcolor,fancyhdr,tikz andhyperref. Both diagrams are embedded TikZ; no external image is missing. The main report is28pages.

QA(17pages) and detailed data extraction(37pages) are separate supporting appendices in03_QA_and_Extraction. The main report presents cross-study analysis; the appendices retain complete paper-level evidence. Neither a polished PDF nor15forms establishes completed final selection.
