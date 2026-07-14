import sqlite3
import hashlib

from database.database import get_connection


def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()



def create_user(username, password):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password
            )

            VALUES (?, ?)

            """,
            (
                username,
                hash_password(password)
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def login_user(username, password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username
        FROM users
        WHERE username = ?
        AND password = ?

        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    conn.close()


    if user:
        return {"id": user[0], "username": user[1]}

    return None