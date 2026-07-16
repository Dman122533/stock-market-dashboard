def format_market_cap(value):

    # ETFs and some assets may not have a market cap
    if value is None:
        return "N/A"

    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"

    elif value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"

    elif value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"

    else:
        return f"${value:,.0f}"