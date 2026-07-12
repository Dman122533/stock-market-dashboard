def get_number_of_holdings(positions):
    """
    Returns number of stocks in portfolio.
    """

    return len(positions)



def get_largest_position(positions):
    """
    Finds the largest holding by value.
    """

    if not positions:
        return None

    largest = max(
        positions,
        key=lambda x:
        x["shares"] * x["price"]
    )

    return largest["ticker"]



def get_average_position_size(positions):
    """
    Calculates average holding value.
    """

    if not positions:
        return 0

    total_value = 0

    for position in positions:

        total_value += (
            position["shares"]
            *
            position["price"]
        )

    return total_value / len(positions)