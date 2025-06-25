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
def activateRun():
    shellScript = f"""
    eval "$(micromamba shell hook --shell=bash)"
    micromamba activate {envName}
    python build.property
    """
    subprocess.run(["bash", "-c", shellScript], check = True)

# parsing 
def main():
    parser = argparse.ArgumentParser(description = "nb2latex CLI tool - convert multiple notebooks to a single LaTeX output")
    parser.add_argument("--build", action = "store_true", help = "Build PDF. Will activate required environment automatically with micromamba")
    parser.add_argument("--env", action = "store_true", help = "Activate (and create if required) environment with micromamba")
    args = parser.parse_args()
    
    if args.env:
        checkMicromamba()
        createEnv()

    if args.build:
        checkMicromamba()
        createEnv()
        activateRun()


if __name__== "__main__":
    main()
