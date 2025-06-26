import subprocess
import argparse
import sys
import os
import shutil
from pathlib import Path
from . import build



def nbconvert(nb):
    print(f"Converting {nb}.ipynb to LaTeX...")
    subprocess.run(["jupyter", "nbconvert", f"{nb}.ipynb", "--to", "latex" ], check = True)

# extract lines between \begin{document} and \end{document} also remove \begin{doucment}, \maketitle, and \end{document} to leave body
def extractTexBody(texFile, bodyFile):
    with open(texFile, 'r') as f:
        lines =f.readlines()            # reads .tex file and stores for processing
    start = None
    end = None
    for i, line in enumerate(lines):
        if r'\begin{document}' in line:
            start = i           # saves line no. for \begin{document}
        elif r'\end{document}' in line:
            end = i             #saves line no. for \end{document}
            break
    if start is None or end is None:
        print(f"Can't find Tex document environment in {texFile}")
        sys.exit(1)
    # extract lines via line numbers
    bodyLines = lines[start+1:end]          # from begin{document} to end{document}, including neither
    # remove \maketitle
    bodyLines = [l for l in bodyLines if r'\maketitle' not in l]
    # make body.tex file (ie no preamble or begin\end{document})
    with open(bodyFile, 'w') as f:
        f.writelines(bodyLines)

def extractPreamble(texFile, preambleFile):
    with open(texFile, 'r') as f:
        lines = f.readlines()
    start = 0
    end = None
    for i, line in enumerate(lines):
        if r'\begin{document}' in line:
            end = i              #saves \begin{document} line no.
            break
    if end is None:
        print(r"Can't find \begin{document}")
        sys.exit(1)     
    # save only up to (not including) \begin{document}
    preamble = lines[start:end]
    with open(preambleFile, 'w') as f:
        f.writelines(preamble)

def compilePDF(texFile):
    print("Compiling PDF")
    # run pdflatex two times to generate table of contents correctly in pdf
    subprocess.run(["pdflatex", texFile], stdout=subprocess. DEVNULL, stderr=subprocess.DEVNULL, check = True)
    subprocess.run(["pdflatex", texFile], stdout=subprocess. DEVNULL, stderr=subprocess.DEVNULL, check = True)

def runBuild(title, notebooks):
    notebookArgs = " ".join(f'"{nb}"' for nb in notebooks)
    shellScript = f"""
    eval "$(micromamba shell hook --shell=bash)"
    micromamba activate {envName}
    python -m nb2latex.build --title "{title}" {notebookArgs}
    """
    subprocess.run(["bash", "-c", shellScript], check=True)

def main():
    parser = argparse.ArgumentParser(description = "nb2latex CLI tool - convert multiple notebooks to a single LaTeX output")
    parser.add_argument("--build", action = "store_true", help = "Build PDF")
    parser.add_argument("--title", default="My Document", help="Document title")
    parser.add_argument("notebooks", nargs="*", help="List of notebooks (.ipynb) to include")
    args = parser.parse_args()

    if args.build:
        runBuild(args.title, args.notebooks)

if __name__== "__main__":
    main()
