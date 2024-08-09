import os
import shutil
import subprocess

from src.toolri.version import VERSION

# variables
name = "ToolRI"
file_name = f"{name}-{VERSION}"
script = "src/toolri/toolri/main.py"
dist_dir = "dist"
output = os.path.join(dist_dir, file_name)
args = "--hidden-import=PIL._tkinter_finder"

# ensure the dist directory exists
os.makedirs(dist_dir, exist_ok=True)


# clean build directories
def clean():
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    if os.path.exists("build"):
        shutil.rmtree("build")
    spec_file = f"{script}.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)


# build the executable
def build():
    subprocess.run(
        [
            "pyinstaller",
            "--name",
            file_name,
            "--onefile",
            script,
            "--specpath",
            dist_dir,
            "--distpath",
            dist_dir,
            "--noconsole",
            "--onefile",
            args,
        ],
        check=True,
    )


# main
def main():
    try:
        import argparse

        parser = argparse.ArgumentParser(description="Build ToolRI using PyInstaller")
        parser.add_argument("command", choices=["all", "clean"], help="Command to run")
        args = parser.parse_args()
        command = args.command
    except:
        command = "build"

    if command == "clean":
        clean()
    else:
        build()


if __name__ == "__main__":
    main()
