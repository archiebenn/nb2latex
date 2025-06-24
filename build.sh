#!/bin/bash


# default title
docTitle='My Document'

# check for --title argument and name document
while [[ "$1" == --* ]]; do
    case "$1" in 
        --title)
            docTitle="$2$"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

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

# add document title to preamble
echo 'Generating master.tex'

# creating master.tex
# nbconvertPreamble.tex taken from nbconverted .tex file (ends at \begin{document})
cat nbconvertPreamble.tex > master.tex

echo '\begin{document}' >> master.tex

# adding \input{} lines for each .tex file
for nb in "${notebooks[@]}"; do
    echo "\clearpage" >> master.tex
    echo "\\section*{$nb}" >> master.tex
    echo "\\input{${nb}_body.tex}" >> master.tex
done

echo '\end{document}' >> master.tex

echo 'Done!'