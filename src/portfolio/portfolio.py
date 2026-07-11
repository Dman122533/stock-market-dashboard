def calculate_position_value(shares, price):
    """
    Calculates the value of a stock position.
    """

    return shares * price



def calculate_portfolio_value(positions):
    """
    Calculates total portfolio value.

    positions:
    [
        {
            "ticker": "AAPL",
            "shares": 10,
            "price": 315
        }
    ]
    """

    total = 0

    for position in positions:
        total += (
            position["shares"]
            *
            position["price"]
        )

    return total



def calculate_allocation(positions):
    """
    Calculates portfolio allocation percentages.
    """

    total_value = calculate_portfolio_value(
        positions
    )

    allocation = {}

    for position in positions:

        value = (
            position["shares"]
            *
            position["price"]
        )

        allocation[position["ticker"]] = (
            value / total_value
        )

    return allocation