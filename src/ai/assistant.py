import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from src.ai.tools import get_stock_information, get_user_portfolio, get_portfolio_analytics, get_stock_risk_metrics, compare_portfolio_risk

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
        {
            "type": "function",
            "name": "get_stock_information",
            "description": (
                "Get current stock or ETF information for a ticker symbol. "
                "Use this when the user asks about a specific stock or ETF."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Ticker symbol such as AAPL, MSFT, SPY, or VOO"
                    }
                },
                "required": ["ticker"],
                "additionalProperties": False
            },
            "strict": True
        },
        {
            "type": "function",
            "name": "get_user_portfolio",
            "description": (
                "Get the logged-in user's portfolio holdings, current values, "
                "cost basis, sectors, and unrealized gains or losses. "
                "Use this when the user asks about their own portfolio."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            },
            "strict": True
        },
        {
            "type": "function",
            "name": "get_portfolio_analytics",
            "description": (
                "Get analytics for the logged-in user's portfolio, including "
                "total portfolio value, largest position, sector allocation, "
                "and total unrealized gain or loss. "
                "Use this when the user asks about their portfolio performance, "
                "concentration, exposure, gains, or overall portfolio statistics."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            },
            "strict": True
        },
        {
            "type": "function",
            "name": "get_stock_risk_metrics",
            "description": (
                "Get risk metrics for a stock or ETF, including volatility, "
                "Sharpe ratio, maximum drawdown, and beta versus the S&P 500. "
                "Use this when the user asks about risk, volatility, drawdown, "
                "Sharpe ratio, or beta for a specific ticker."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Ticker symbol such as AAPL, MSFT, SPY, or JPM"
                    },
                    "period": {
                        "type": "string",
                        "description": (
                            "Historical period such as 1mo, 6mo, 1y, or 5y."
                        )
                    }
                },
                "required": ["ticker"],
                "additionalProperties": False
            },
            "strict": False
        },
        {
            "type": "function",
            "name": "compare_portfolio_risk",
            "description": (
                "Compare risk metrics across all holdings in the logged-in user's portfolio. "
                "Use this when the user asks which holding is riskiest, has the highest beta, "
                "highest volatility, worst drawdown, best Sharpe ratio, or asks to rank portfolio holdings by risk."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "period": {
                        "type": "string",
                        "description": "Historical period such as 1mo, 6mo, 1y, or 5y."
                    }
                },
                "required": [],
                "additionalProperties": False
            },
            "strict": False
        }
    ]
def ask_financial_assistant(
        user_message,
        context="",
        user_id=None
    ):
        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions=(
                "You are an AI financial education assistant inside a stock market dashboard. "
                "Use available tools when the user asks about specific securities or application data. "
                "Explain financial information clearly and concisely. "
                "Do not invent financial data. "
                "Do not present responses as personalized financial advice."
            ),
            input=f"""
    User question:
    {user_message}

    Application context:
    {context}
    """,
            tools=tools
        )

        tool_outputs = []

        for item in response.output:

            if item.type == "function_call":

                if item.name == "get_stock_information":

                    arguments = json.loads(
                        item.arguments
                    )

                    result = get_stock_information(
                        arguments["ticker"]
                    )

                    tool_outputs.append(
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": json.dumps(result)
                        }
                    )

                elif item.name == "get_user_portfolio":

                    if user_id is None:
                        result = {
                            "error": "No logged-in user is available."
                        }

                    else:
                        result = get_user_portfolio(
                            user_id
                        )

                    tool_outputs.append(
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": json.dumps(result)
                        }
                    )
                elif item.name == "get_portfolio_analytics":

                    if user_id is None:
                        result = {
                            "error": "No logged-in user is available."
                        }

                    else:
                        result = get_portfolio_analytics(
                            user_id
                        )

                    tool_outputs.append(
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": json.dumps(result)
                        }
                    )
                elif item.name == "get_stock_risk_metrics":

                    arguments = json.loads(
                        item.arguments
                    )

                    result = get_stock_risk_metrics(
                        arguments["ticker"],
                        arguments.get("period", "1y")
                    )

                    tool_outputs.append(
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": json.dumps(result)
                        }
                    )
                elif item.name == "compare_portfolio_risk":

                    arguments = json.loads(
                        item.arguments
                    )

                    if user_id is None:
                        result = {
                            "error": "No logged-in user is available."
                        }

                    else:
                        result = compare_portfolio_risk(
                            user_id,
                            arguments.get("period", "1y")
                        )

                    tool_outputs.append(
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": json.dumps(result)
                        }
                    )
        if tool_outputs:

            response = client.responses.create(
                model="gpt-5.6-luna",
                instructions=(
                    "You are an AI financial education assistant. "
                    "Use the tool results to answer the user's question clearly. "
                    "Do not invent missing data. "
                    "Format currency values normally, for example $493.95. "
                    "Use clean Markdown formatting."
                ),
                previous_response_id=response.id,
                input=tool_outputs
            )

        return response.output_text