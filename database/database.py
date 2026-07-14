import sqlite3


DATABASE_NAME = "portfolio.db"


def get_connection():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    return conn


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS holdings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            ticker TEXT NOT NULL,

            shares REAL NOT NULL,

            price REAL,

            cost_basis REAL,

            sector TEXT

        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
        """
    )


    conn.commit()

    conn.close()
def add_holding(user_id, ticker, shares, price, cost_basis, sector):
    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO holdings
        (
            user_id,
            ticker,
            shares,
            price,
            cost_basis,
            sector
        )

        VALUES (?, ?, ?, ?, ?, ?)

        """,
        (
            user_id,
            ticker,
            shares,
            price,
            cost_basis,
            sector
        )
    )


    conn.commit()

    conn.close()
def get_holdings(user_id):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT ticker, shares, price, cost_basis, sector
        FROM holdings
        WHERE user_id = ?
        """,
        (user_id,)
    )


    rows = cursor.fetchall()


    conn.close()


    holdings = []


    for row in rows:

        holdings.append(
            {
                "ticker": row[0],
                "shares": row[1],
                "price": row[2],
                "cost_basis": row[3],
                "sector": row[4]
            }
        )


    return holdings

def remove_holding(user_id, ticker):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM holdings
        WHERE ticker = ?
        AND user_id = ?
        """,
        (ticker, user_id)
    )

    conn.commit()

    conn.close()

def update_holding(user_id, ticker, shares, price, cost_basis, sector):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE holdings

        SET
            shares = ?,
            price = ?,
            cost_basis = ?,
            sector = ?

        WHERE ticker = ?
        AND user_id = ?

        """,
        (
            shares,
            price,
            cost_basis,
            sector,
            ticker,
            user_id
        )
    )


    conn.commit()

    conn.close()

def update_price(user_id, ticker, price):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE holdings

        SET price = ?

        WHERE ticker = ?
        AND user_id = ?
        """,
        (
            price,
            ticker,
            user_id
        )
    )


    conn.commit()

    conn.close()

