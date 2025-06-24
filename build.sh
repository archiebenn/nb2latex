#!/bin/bash


# default title
docTitle='My Document'

# check for --title argument and name document. shift so $@ only .ipynbs
while [[ "$1" == --* ]]; do
    case "$1" in 
        --title)
            docTitle="$2"
            shift 2
            ;;
        *)
            #catch any flag typos
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# make directory for output files
outputDir="${docTitle} files"
mkdir -p "$outputDir"


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

    # take main body of each individual .tex file (and remove \begin{document}, \maketitle and \end{document} of each)
    sed -n '/\\begin{document}/, /\\end{document}/p' "$nb.tex" | sed -e '1d' -e '3d' -e '$d' > "$nb"_body.tex
done

# extract preamble from first notebook (nbconvert preamble) and create preamble.tex file
nbOne="${notebooks[0]}"
# takes preamble up to and including \begin{document}, then pipe deletes '\begin{document}
sed '/\\begin{document}/q' "${nbOne}.tex" | sed '$d' > "$docTitle.tex"


# add document extras post-preamble
echo "\\title{$docTitle}" >> "$docTitle.tex"
echo '\begin{document}' >> "$docTitle.tex"
echo "\\maketitle" >> "$docTitle.tex"
echo '\tableofcontents' >> "$docTitle.tex"

# adding \input{} lines for each .tex file
for nb in "${notebooks[@]}"; do
    echo "\clearpage" >> "$docTitle.tex"
    echo "\\input{${nb}_body.tex}" >> "$docTitle.tex"
done

echo '\end{document}' >> "$docTitle.tex"

pdflatex "$docTitle.tex"

# move output files to document directory
mv "$docTitle".{aux,log,out,toc,tex} "$outputDir"/
mv *_body.tex "$outputDir"

echo 'Done!'