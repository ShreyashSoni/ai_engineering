#!/bin/bash
# Run script for Company Brochure Generator
# This script sets up the environment and launches the app

# Set library path for WeasyPrint on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_FALLBACK_LIBRARY_PATH"
fi

# Run the application
python app.py