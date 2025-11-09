#!/usr/bin/env python3
"""
AI Governance Pro - Main Entry Point
"""

import sys
import os

# Add the current directory to Python path so we can import from src
sys.path.insert(0, os.path.dirname(__file__))

try:
    # Import and run the main application
    from src.app.main import main
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("This usually means there are still import path issues.")
    print("Please run the import fixer scripts first.")
    sys.exit(1)
except Exception as e:
    print(f"❌ Application Error: {e}")
    sys.exit(1)
