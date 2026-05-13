from database.db import conn, cursor

# =========================================
# CREATE USER
# =========================================
def create_user(user_id):

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    if user is None:

        cursor.execute(
            "INSERT INTO users (user_id) VALUES (?)",
            (user_id,)
        )

        conn.commit()


# =========================================
# GET BALANCE
# =========================================
def get_balance(user_id):

    create_user(user_id)

    cursor.execute(
        "SELECT balance FROM users WHERE user_id = ?",
        (user_id,)
    )

    balance = cursor.fetchone()[0]

    return balance


# =========================================
# ADD COINS
# =========================================
def add_coins(user_id, amount):

    create_user(user_id)

    cursor.execute(
        """
        UPDATE users
        SET balance = balance + ?
        WHERE user_id = ?
        """,
        (amount, user_id)
    )

    conn.commit()


# =========================================
# REMOVE COINS
# =========================================
def remove_coins(user_id, amount):

    create_user(user_id)

    current = get_balance(user_id)

    if current < amount:

        return False

    cursor.execute(
        """
        UPDATE users
        SET balance = balance - ?
        WHERE user_id = ?
        """,
        (amount, user_id)
    )

    conn.commit()

    return True


# =========================================
# SET LAST DAILY
# =========================================
def set_last_daily(user_id, timestamp):

    create_user(user_id)

    cursor.execute(
        """
        UPDATE users
        SET last_daily = ?
        WHERE user_id = ?
        """,
        (timestamp, user_id)
    )

    conn.commit()


# =========================================
# GET LAST DAILY
# =========================================
def get_last_daily(user_id):

    create_user(user_id)

    cursor.execute(
        "SELECT last_daily FROM users WHERE user_id = ?",
        (user_id,)
    )

    return cursor.fetchone()[0]
