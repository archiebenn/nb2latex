# nb2latex

Convert multiple Jupyter notebooks into a single, LaTeX document and PDF.

## Overview

`nb2latex` is a lightweight Python CLI tool that takes multiple `.ipynb` files and combines them into one polished LaTeX document. It removes boilerplate, extracts the useful content, and compiles it into a single PDF with a title page and table of contents.

Great for generating clean reports, academic writeups, or notebooks with a consistent output format.

---

## Features

- Converts `.ipynb` notebooks to LaTeX using `nbconvert`
- Strips unnecessary LaTeX preamble and metadata
- Combines multiple notebook bodies into one document
- Adds title page and table of contents automatically
- Compiles the final `.tex` to PDF using `pdflatex`
- Cleans up intermediate files

---

## Requirements

- Python 3.7+
- [Pandoc](https://pandoc.org) (required for `nbconvert`)
- `pdflatex` (e.g. from TeX Live or MiKTeX)

Install dependencies:

```bash
pip install nb2latex

