import sqlite3

# =========================================
# CONNECT DATABASE
# =========================================
conn = sqlite3.connect(
    "casino.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =========================================
# USERS TABLE
# =========================================
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (

        user_id INTEGER PRIMARY KEY,

        balance INTEGER DEFAULT 1000,

        last_daily REAL DEFAULT 0
    )
    """
)

conn.commit()