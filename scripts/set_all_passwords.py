"""
Set all user passwords to the provided password (use for emergency recovery only).
Usage:
  python scripts/set_all_passwords.py 1234
This uses the same hashing function as `backend/auth.py`.
"""
import sys
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))

try:
    from auth import hash_password
except Exception as e:
    print('Failed to import auth.hash_password:', e)
    raise

DB_PATH = ROOT / 'backend' / 'mortgage.db'

if len(sys.argv) < 2:
    print('Usage: python scripts/set_all_passwords.py NEW_PASSWORD')
    sys.exit(1)

newpw = sys.argv[1]

if not DB_PATH.exists():
    print('Database not found at', DB_PATH)
    sys.exit(1)

pw_hash, salt = hash_password(newpw)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute('SELECT username FROM users')
users = [r[0] for r in cursor.fetchall()]
for u in users:
    cursor.execute('UPDATE users SET password_hash = ?, password_salt = ? WHERE username = ?', (pw_hash, salt, u))
print(f'Updated {len(users)} users to the new password')
conn.commit()
conn.close()
print('Done. Users updated:', users)
