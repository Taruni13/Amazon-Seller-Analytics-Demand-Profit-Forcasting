#!/usr/bin/env python3
"""
Launcher script: run the Streamlit app from plain Python without importing
Streamlit inside the same process (avoids the "Runtime instance already exists" error).

Usage:
    python run_app.py [-- [streamlit-args]]

Example:
    python run_app.py -- --server.port 8502
"""
import os
import shutil
import subprocess
import sys

def main():
    if shutil.which("streamlit") is None:
        print("Error: `streamlit` is not installed or not on PATH. Install with: pip install streamlit")
        sys.exit(1)

    # Forward any args after `--` to streamlit
    extra = []
    if "--" in sys.argv:
        idx = sys.argv.index("--")
        extra = sys.argv[idx+1:]

    cmd = [shutil.which("streamlit"), "run", "app.py"] + extra
    return subprocess.call(cmd)

if __name__ == '__main__':
    sys.exit(main())
