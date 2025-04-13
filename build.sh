#!/bin/bash

# Ensure the script exits if any command fails
set -e

# Create a virtual environment if it doesn't exist
if [ ! -d "env" ]; then
  python3 -m venv env
fi

# Activate the virtual environment
source env/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install the required packages
pip install -r requirements.txt
pip install pyinstaller

# Define the name of the executable
EXECUTABLE_NAME="PygTris"

# Navigate to the directory containing this script
cd "$(dirname "$0")"

# Remove previous build artifacts if they exist
rm -rf build/ dist/ "$EXECUTABLE_NAME.spec"

# Run PyInstaller to create a one-file Windows executable
pyinstaller \
  --onefile \
  --name "$EXECUTABLE_NAME" \
  --distpath . \
  src/main.py
