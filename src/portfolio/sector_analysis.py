def calculate_sector_allocation(positions):
    """
    Calculates portfolio allocation by sector.
    """

    sector_values = {}

    total_value = 0


    for position in positions:

        value = (
            position["shares"]
            *
            position["price"]
        )

        total_value += value


        sector = position["sector"]

        if sector in sector_values:

            sector_values[sector] += value

        else:

            sector_values[sector] = value


    sector_allocation = {}


    for sector, value in sector_values.items():

        sector_allocation[sector] = (
            value / total_value
        )


    return sector_allocation