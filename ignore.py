import subprocess
import argparse
import os
import sys
import shutil

def convert_notebook_to_tex(nb):
    print(f"Converting {nb}.ipynb to LaTeX file...")
    subprocess.run(["jupyter", "nbconvert", f"{nb}.ipynb", "--to", "latex"], check=True)

def extract_body(tex_file, body_file):
    # Extract lines between \begin{document} and \end{document} but remove \begin{document}, \maketitle and \end{document}
    with open(tex_file, 'r') as f:
        lines = f.readlines()

    start = None
    end = None
    for i, line in enumerate(lines):
        if r'\begin{document}' in line:
            start = i
        elif r'\end{document}' in line:
            end = i
            break

    if start is None or end is None:
        print(f"Error: Cannot find document environment in {tex_file}")
        sys.exit(1)

    # extract lines between start and end
    body_lines = lines[start+1:end]

    # remove \maketitle line if present
    body_lines = [l for l in body_lines if r'\maketitle' not in l]

    with open(body_file, 'w') as f:
        f.writelines(body_lines)

def extract_preamble(tex_file, output_file):
    # Copy lines from beginning until (and including) \begin{document}, excluding the \begin{document} line itself
    with open(tex_file, 'r') as f:
        lines = f.readlines()

    preamble_lines = []
    for line in lines:
        preamble_lines.append(line)
        if r'\begin{document}' in line:
            # remove \begin{document} line
            preamble_lines.pop()
            break

    with open(output_file, 'w') as f:
        f.writelines(preamble_lines)

def compile_pdf(tex_file):
    print("Compiling LaTeX...")
    # Run pdflatex twice for TOC
    subprocess.run(["pdflatex", tex_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    subprocess.run(["pdflatex", tex_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def main():
    parser = argparse.ArgumentParser(description="Build PDF from multiple Jupyter notebooks via LaTeX")
    parser.add_argument("--title", default="My Document", help="Document title")
    parser.add_argument("notebooks", nargs="+", help="List of notebooks (.ipynb) to merge")
    args = parser.parse_args()

    doc_title = args.title
    notebooks = [os.path.splitext(nb)[0] for nb in args.notebooks]  # strip .ipynb

    output_dir = f"{doc_title} files"
    os.makedirs(output_dir, exist_ok=True)

    # Convert each notebook and extract body
    for nb in notebooks:
        convert_notebook_to_tex(nb)
        extract_body(f"{nb}.tex", f"{nb}Body.tex")

    # Extract preamble from first notebook
    extract_preamble(f"{notebooks[0]}.tex", f"{doc_title}.tex")

    # Append title, begin document, maketitle, TOC
    with open(f"{doc_title}.tex", "a") as f:
        f.write(f"\\title{{{doc_title}}}\n")
        f.write("\\begin{document}\n")
        f.write("\\maketitle\n")
        f.write("\\tableofcontents\n")

        # Add inputs with clearpage
        for nb in notebooks:
            f.write("\\clearpage\n")
            f.write(f"\\input{{{nb}Body.tex}}\n")

        f.write("\\end{document}\n")

    # Compile PDF
    compile_pdf(f"{doc_title}.tex")

    # Move auxiliary and output files to output_dir
    for ext in ["aux", "log", "out", "toc", "tex", "pdf"]:
        file_name = f"{doc_title}.{ext}"
        if os.path.exists(file_name):
            shutil.move(file_name, os.path.join(output_dir, file_name))

    print(f"PDF compiling complete! Output: {os.path.join(output_dir, doc_title)}.pdf")

if __name__ == "__main__":
    main()
