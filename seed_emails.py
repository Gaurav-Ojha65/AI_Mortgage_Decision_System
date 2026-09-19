import sqlite3
import os

db_path = os.path.join('backend', 'mortgage.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Update existing users without emails
cursor.execute("UPDATE users SET email = username || '@mortgage.ai' WHERE email IS NULL")
print(f"Updated {cursor.rowcount} users with default emails.")

conn.commit()
conn.close()
