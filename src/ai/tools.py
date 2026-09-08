from database.database import get_holdings
from src.api.stock_api import get_stock_data
from src.portfolio.portfolio import calculate_portfolio_value
from src.portfolio.portfolio_metrics import get_largest_position
from src.portfolio.sector_analysis import calculate_sector_allocation
from src.api.stock_api import get_stock_history
from src.analytics.risk_metrics import calculate_sharpe_ratio, calculate_max_drawdown, calculate_beta
from src.analytics.stock_metrics import calculate_volatility


def get_stock_information(ticker: str):
    stock = get_stock_data(ticker.upper())

    if stock is None or stock["price"] is None:
        return {
            "error": "Unable to retrieve stock information."
        }

    return {
        "ticker": ticker.upper(),
        "name": stock.get("name"),
        "price": stock.get("price"),
        "previous_close": stock.get("previous_close"),
        "market_cap": stock.get("market_cap"),
        "sector": stock.get("sector"),
        "52_week_high": stock.get("52_week_high"),
        "52_week_low": stock.get("52_week_low"),
        "asset_type": stock.get("asset_type")
    }


def get_user_portfolio(user_id: int):
    holdings = get_holdings(user_id)

    if not holdings:
        return {
            "message": "The user does not currently have any holdings.",
            "holdings": []
        }

    portfolio = []

    total_value = 0

    for holding in holdings:
        position_value = (
            holding["shares"]
            *
            holding["price"]
        )

        total_value += position_value

        unrealized_gain = (
            holding["price"]
            -
            holding["cost_basis"]
        ) * holding["shares"]

        portfolio.append(
            {
                "ticker": holding["ticker"],
                "shares": holding["shares"],
                "current_price": holding["price"],
                "cost_basis": holding["cost_basis"],
                "sector": holding["sector"],
                "position_value": position_value,
                "unrealized_gain": unrealized_gain
            }
        )

    return {
        "total_portfolio_value": total_value,
        "holdings": portfolio
    }
def get_portfolio_analytics(user_id: int):
    holdings = get_holdings(user_id)

    if not holdings:
        return {
            "message": "The user does not currently have any holdings."
        }

    total_value = calculate_portfolio_value(
        holdings
    )

    largest_position = get_largest_position(
        holdings
    )

    sector_allocation = calculate_sector_allocation(
        holdings
    )

    total_unrealized_gain = 0

    for holding in holdings:
        unrealized_gain = (
            holding["price"]
            -
            holding["cost_basis"]
        ) * holding["shares"]

        total_unrealized_gain += unrealized_gain

    return {
        "total_portfolio_value": total_value,
        "largest_position": largest_position,
        "sector_allocation": sector_allocation,
        "total_unrealized_gain": total_unrealized_gain
    }
def get_stock_risk_metrics(ticker: str, period: str = "1y"):
    """
    Retrieves risk metrics for a stock or ETF.
    """

    ticker = ticker.upper()

    history = get_stock_history(
        ticker,
        period
    )

    if history is None or history.empty:
        return {
            "error": f"Unable to retrieve historical data for {ticker}."
        }

    market_history = get_stock_history(
        "^GSPC",
        period
    )

    volatility = calculate_volatility(
        history
    )

    sharpe_ratio = calculate_sharpe_ratio(
        history
    )

    max_drawdown = calculate_max_drawdown(
        history
    )

    beta = calculate_beta(
        history,
        market_history
    )

    return {
        "ticker": ticker,
        "period": period,
        "volatility": volatility,
        "sharpe_ratio": sharpe_ratio,
        "maximum_drawdown": max_drawdown,
        "beta_vs_sp500": beta
    }
def compare_portfolio_risk(user_id: int, period: str = "1y"):
    holdings = get_holdings(user_id)

    if not holdings:
        return {
            "message": "The user does not currently have any holdings.",
            "holdings": []
        }

    results = []

    for holding in holdings:
        ticker = holding["ticker"]

        history = get_stock_history(
            ticker,
            period
        )

        if history is None or history.empty:
            results.append(
                {
                    "ticker": ticker,
                    "error": "Unable to retrieve historical data."
                }
            )
            continue

        market_history = get_stock_history(
            "^GSPC",
            period
        )

        volatility = calculate_volatility(
            history
        )

        sharpe_ratio = calculate_sharpe_ratio(
            history
        )

        max_drawdown = calculate_max_drawdown(
            history
        )

        beta = calculate_beta(
            history,
            market_history
        )

        results.append(
            {
                "ticker": ticker,
                "volatility": volatility,
                "sharpe_ratio": sharpe_ratio,
                "maximum_drawdown": max_drawdown,
                "beta_vs_sp500": beta
            }
        )

    return {
        "period": period,
        "holdings": results
    }