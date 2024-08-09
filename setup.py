from setuptools import setup

VERSION_FILE = "./src/toolri/version.py"
with open(VERSION_FILE, "r") as file:
    for line in file:
        if line.startswith("VERSION"):
            VERSION = line.split("=")[1].strip().strip('"').strip("'")

setup(
    version=VERSION,
)
