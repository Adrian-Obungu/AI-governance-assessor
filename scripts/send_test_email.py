#!/usr/bin/env python3
"""Send a test email using the configured email sender.

Usage:
  python scripts/send_test_email.py recipient@example.com

If SMTP is not enabled, the token will be logged to the console (development fallback).
"""
import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)

def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/send_test_email.py recipient@example.com')
        sys.exit(1)

    to_email = sys.argv[1]
    try:
        from modules.utils.email_sender import send_reset_email
        # send a dummy token
        token = 'TEST-TOKEN-12345'
        sent, err = send_reset_email(to_email, token)
        if sent:
            print(f'Successfully sent test email (or logged token) to {to_email}')
        else:
            print(f'Failed to send test email: {err}')
    except Exception as e:
        print('Error importing email sender or sending email:', e)
        raise

if __name__ == '__main__':
    main()
