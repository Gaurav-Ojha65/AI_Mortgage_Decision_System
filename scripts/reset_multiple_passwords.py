"""
Reset multiple user passwords in the backend SQLite database.
Usage:
  - Edit the `PASSWORD_MAP` below with username: password pairs, or
  - Run with a CSV path: `python scripts/reset_multiple_passwords.py users.csv`
CSV format: username,new_password (no header)

This script uses the same hashing function as `backend/auth.py` so passwords are compatible.
"""
import sys
import sqlite3
from pathlib import Path

# Ensure backend module imports work
ROOT = Path(__file__).resolve().parents[1]
import os
sys.path.insert(0, str(ROOT / 'backend'))

try:
    from auth import hash_password
except Exception as e:
    print('Failed to import auth.hash_password:', e)
    raise

DB_PATH = ROOT / 'backend' / 'mortgage.db'

# Example mapping - edit this or provide a CSV file as argv[1]
PASSWORD_MAP = {
    # username: new_password
    'none': 'ResetPass1!',
    'gaurav': 'ResetPass1!',
    'pal': 'ResetPass1!',
}


def read_csv(path):
    m = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or ',' not in line:
                continue
            u, p = line.split(',', 1)
            m[u.strip()] = p.strip()
    return m


def update_passwords(mapping):
    if not DB_PATH.exists():
        print('Database not found at', DB_PATH)
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for username, newpw in mapping.items():
        pw_hash, salt = hash_password(newpw)
        cursor.execute('SELECT id, username FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        if not row:
            print(f'User not found: {username}')
            continue
        cursor.execute('UPDATE users SET password_hash = ?, password_salt = ? WHERE username = ?', (pw_hash, salt, username))
        print(f'Updated password for {username}')
    conn.commit()
    # verify
    cursor.execute('SELECT username, full_name, is_active FROM users')
    rows = cursor.fetchall()
    print('\nCurrent users in DB:')
    for r in rows:
        print(r)
    conn.close()


if __name__ == '__main__':
    mapping = PASSWORD_MAP.copy()
    if len(sys.argv) > 1:
        csvpath = Path(sys.argv[1])
        if csvpath.exists():
            mapping = read_csv(csvpath)
        else:
            print('CSV path not found:', csvpath)
            sys.exit(1)
    if not mapping:
        print('No users to update')
        sys.exit(0)
    update_passwords(mapping)
