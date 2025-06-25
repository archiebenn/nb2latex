import subprocess
import argparse
import sys
import os
import shutil
from pathlib import Path

envName = "nb2latex"
envFile = "environment.yml"


# check if micromamba installed
def checkMicromamba():
    if not shutil.which("micromamba"):
        print("micromamba not found in PATH")
        sys.exit(1)


# create env if required (no shell involved)
def createEnv(): 
    result = subprocess.run(
        ["micromamba", "env", "list"], 
        captureOutput = True, text = True
    )

    if envName not in result.stdout:
        print(f"Creating '{envName}' environment) from {envFile}...")
        subprocess.run([
            "micromamba", "create", "-y", "-n", envName, "-f", envFile
            ], check = True)
    else:
        print(f"{envFile} environment exists")


# activate env and run build.py (shell involved - spawn a subprocess)
# also builds build.py based on arguments passed to nb2latex.py
def activateRun(title, notebooks):
    notebookArgs = " ".join(f'"{nb}"' for nb in notebooks)          # wrap notebook filenames in double quotes for shell
    
    # runs build.py with args from CLI
    shellScript = f"""
    eval "$(micromamba shell hook --shell=bash)"
    micromamba activate {envName}
    python build.py --title {title} {notebookArgs} 
    """
    subprocess.run(["bash", "-c", shellScript], check = True)


# parsing 
def main():
    parser = argparse.ArgumentParser(description = "nb2latex CLI tool - convert multiple notebooks to a single LaTeX output")
    parser.add_argument("--build", action = "store_true", help = "Build PDF. Will activate required environment automatically with micromamba")
    parser.add_argument("--env", action = "store_true", help = "Activate (and create if required) environment with micromamba")
    parser.add_argument("--title", default="My Document", help="Document title")
    parser.add_argument("notebooks", nargs="*", help="List of notebooks (.ipynb) to include")
    args = parser.parse_args()
    
    if args.env:
        checkMicromamba()
        createEnv()

    if args.build:
        checkMicromamba()
        createEnv()
        activateRun(args.title, args.notebooks)


if __name__== "__main__":
    main()
