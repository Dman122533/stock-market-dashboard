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

            ticker TEXT NOT NULL,

            shares REAL NOT NULL,

            price REAL,

            sector TEXT

        )
        """
    )


    conn.commit()

    conn.close()
def add_holding(ticker, shares, price, sector):
    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO holdings
        (
            ticker,
            shares,
            price,
            sector
        )

        VALUES (?, ?, ?, ?)

        """,
        (
            ticker,
            shares,
            price,
            sector
        )
    )


    conn.commit()

    conn.close()
def get_holdings():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT ticker, shares, price, sector
        FROM holdings
        """
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
                "sector": row[3]
            }
        )


    return holdings

def remove_holding(ticker):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM holdings
        WHERE ticker = ?
        """,
        (ticker,)
    )

    conn.commit()

    conn.close()

def update_holding(ticker, shares, price, sector):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE holdings

        SET
            shares = ?,
            price = ?,
            sector = ?

        WHERE ticker = ?

        """,
        (
            shares,
            price,
            sector,
            ticker
        )
    )


    conn.commit()

    conn.close()

def update_price(ticker, price):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE holdings

        SET price = ?

        WHERE ticker = ?

        """,
        (
            price,
            ticker
        )
    )


    conn.commit()

    conn.close()