# 📈 Stock Market Dashboard

A full-stack personal finance and portfolio analytics application built with Python and Streamlit. This application allows users to analyze individual stocks, manage personal investment portfolios, and evaluate portfolio performance using financial metrics and benchmark comparisons.

## Features

### Stock Analysis Dashboard
- Search stocks using ticker symbols
- View current stock information:
  - Current price
  - Previous close
  - Market capitalization
  - Sector
  - 52-week high/low
- Interactive price history charts
- Candlestick visualization
- 20-day and 50-day moving averages
- Trading volume analysis

### Portfolio Management
- Create a personal investment portfolio
- Add stock holdings
- Support fractional shares
  - Example: 16.25 shares
- Update existing holdings
- Remove holdings
- Refresh current stock prices
- Portfolio allocation visualization
- Sector allocation analysis

### Portfolio Analytics
- Portfolio value tracking
- Total return calculation
- Volatility analysis
- Sharpe ratio
- Maximum drawdown
- Best/worst trading days
- Beta comparison against the S&P 500
- Benchmark performance comparison

### User Authentication
- User account creation
- Secure password hashing
- Login/logout functionality
- Individual user portfolio storage
- SQLite database integration

---

# Technologies Used

## Programming Language
- Python

## Framework
- Streamlit

## Data Processing
- Pandas
- NumPy

## Financial Data
- Yahoo Finance API (`yfinance`)

## Visualization
- Plotly

## Database
- SQLite

## Development Tools
- Git
- GitHub
- Virtual environments

---

# Running the Application Locally

Follow these steps to run the Stock Market Dashboard on your own computer.

## Prerequisites

Before starting, make sure you have installed:

- Python 3.10 or newer
- Git
- A code editor (optional, recommended: Visual Studio Code)

You can verify Python is installed by running:

```bash
python --version
```

## Installation Instructions
### Clone the Repository 
Open a terminal and run: 
```bash

git clone https://github.com/Dman122533/stock-market-dashboard

```
### Navigate to project folder
```bash
cd stock-market-dashboard
```
### Create Virtual Environment
windows: 
``` bash
python -m venv .venv
```
Mac/Linux: 
```bash
python3 -m venv .venv
```
### Activate the Virtual Environment
Windows: 
```bash
.venv\Scripts\activate
```
Mac/Linux: 
```bash
source .venv/bin/activate
```
### Install Required Packages
```bash
pip install -r requirements.txt
```
### Start Application
```bash
streamlit run app.py
```
The application will open automatically in your browser.

If it does not, open:

http://localhost:8501

### To Stop Application
ctrl + c in terminal window