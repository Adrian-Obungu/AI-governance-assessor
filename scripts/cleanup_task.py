#!/usr/bin/env python3
"""Run database cleanup for expired password reset tokens and old requests.

This script is intended to be called from a scheduler (cron/GitHub Actions).
"""
import os
import sys

# Ensure src/ is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)

def main():
    try:
        from modules.auth.auth_manager import auth_manager
        auth_manager.cleanup_expired_tokens()
        print('Cleanup completed successfully.')
    except Exception as e:
        print('Cleanup failed:', e)
        raise

if __name__ == '__main__':
    main()
