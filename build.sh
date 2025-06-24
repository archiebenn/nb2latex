#!/bin/bash

# check if arguments provided
if [ $# -eq 0 ]; then
    echo 'Usage: $0 notebook1.ipynb notebook2.ipynb ...'
    exit 1
fi

# create array for args to go into and remove .ipynb for the array
notebooks=()
for arg in "$@"; do
    # strip .ipynb from filename
    filename="${arg%.ipynb}"
    notebooks+=("$filename")
done

# loop over notebook array and use nbconvert to convert to .tex
for nb in "${notebooks[@]}"; do
    echo "Converting $nb.ipynb to LaTeX file..."
    jupyter nbconvert "$nb.ipynb" --to latex
    # take main body of each individual .tex file (and remove \begin{document} and \end{document} of each)
    sed -n '/\\begin{document}/, /\\end{document}/p' "$nb.tex" | sed '1d;$d' > "$nb"_body.tex
done

# generate master.tex
echo 'Generating master.tex'

# creating master.tex
# nbconvertPreamble.tex taken from nbconverted .tex file (ends at \begin{document})
cat nbconvertPreamble.tex > master.tex

# adding \input{} lines for each .tex file
for nb in "${notebooks[@]}"; do
    echo "\\section*{$nb}" >> master.tex
    echo "\\input{$nb}_body.tex" >> master.tex
done

echo '\\end{document}' >> master.tex

echo 'Done!'