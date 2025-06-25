import subprocess
import sys
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
        captureOutput = True,
        text = True
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

if __name__== "__main__":
    checkMicromamba()
    createEnv()
    activateRun()

