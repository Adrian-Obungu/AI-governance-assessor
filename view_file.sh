#!/bin/bash
# File Viewer Script for AI Governance Pro
# Usage: ./view_file.sh <file_path>

if [ $# -eq 0 ]; then
    echo "Usage: ./view_file.sh <file_path>"
    echo "Example: ./view_file.sh src/app/main.py"
    exit 1
fi

FILE_PATH=$1

if [ -f "$FILE_PATH" ]; then
    echo "=== Contents of $FILE_PATH ==="
    cat "$FILE_PATH"
    echo "=== End of $FILE_PATH ==="
else
    echo "Error: File $FILE_PATH not found"
    echo "Available Python files:"
    find src -name "*.py" | head -20
fi
