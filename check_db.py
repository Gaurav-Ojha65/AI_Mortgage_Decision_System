import sqlite3
conn = sqlite3.connect('backend/mortgage.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(users)")
print("USERS TABLE:", cursor.fetchall())
cursor.execute("PRAGMA table_info(audit_logs)")
print("AUDIT LOGS TABLE:", cursor.fetchall())
conn.close()
