#!/bin/bash

# Get the parent directory of the current script and change the current directory to it
SCRIPT_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PARENT_DIR"

if [ ! -f "venv/bin/activate" ]; then
    python3.12 -m venv venv
fi

source venv/bin/activate

python3.12 -m pip install --upgrade pip

pip install -r requirements.txt

python -m streamlit run scripts/streamlit_app.py --server.port 8787 --browser.serverAddress localhost
