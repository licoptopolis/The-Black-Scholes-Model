"""
Black Scholes Model using yFinance API
Assumptions for this calculator:
European options that can only be exercised at expiration
No dividends to be paid out during the options' lifespan
The return on the underlying are normally distributed
"""
"""
variable Sample
    R = 0.01        # Interest Rate
    S = 30          # underlying Price
    K = 10          # Strike Price
    T = 252/365     # Time to Maturity
    sigma = 0.30    # Volatility
"""

"""Importing Necessary Libraries"""
import numpy as np
import yfinance as yf
from scipy.stats import norm

"""Defining User Inputs"""
def inputs():
    symbol = input("Stock/Ticker: ")    # User Inputs the Stock of Choice
    stock_data = yf.download(symbol)    # Programme Downloads Data for Chosen Stock
    X = stock_data["Adj Close"][-1]     # Retrieve most recent closing price

    S = None
    while S is None:
        S = round(X, 2)     # Round Stock Price to 2 Decimal Places
        print("Underlying Price: " , round(X, 2))

    interest_rate = ("^TNX")                            # COBE 10 YR TREASURY NOTE YIELD
    interest_rate_data = yf.download(interest_rate)
    R = interest_rate_data["Adj Close"][-1]
    round(R, 2)

    K = None
    while K is None:
        try:
            K = float(input("Strike Price: "))
        except ValueError:
            print("\033[1mInvalid input. Please enter a valid value.\033[m")

    T = None
    while T is None:
        try:
            T = eval(input("Time to Maturity (Displayed as 000/35): "))
        except (NameError, SyntaxError):
            print("\033[1mInvalid input. Please enter a valid value.\033[m")

    volatility = ("^VIX")               
    vix_data = yf.download(volatility)  # Programme Downloads Data for VIX
    sigma = vix_data["Adj Close"][-1]   # Retrieve most recent closing price
    round(sigma, 2)

    option_type = None
    while option_type is None:
        option_type = input("Do you wish to calculate a Call or a Put? Answer 'C' for Call and 'P' for Put: ").upper()
        if option_type not in ["C", "P"]:
            print("\033[1mInvalid input. Please enter a valid value.\033[m")

    return symbol, stock_data, R, S, K, T, sigma, option_type

"""Black Scholes Model"""
def black_scholes(symbol, stock_data, R, S, K, T, sigma, option_type):
    """Calculate option price for calls or puts"""
    recent_stock_price = stock_data["Adj Close"][-1]
    """Formula:"""
    d1 = (np.log(S / K) + (R + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "C":
        price = S * norm.cdf(d1) - K * np.exp(-R * T) * norm.cdf(d2)
    elif option_type == "P":
        price = K * np.exp(-R * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Choose 'C' for call or 'P' for put.")
    return price

symbol, stock_data, R, S, K, T, sigma, option_type = inputs()
option_price = black_scholes(symbol, stock_data, R, S, K, T, sigma, option_type)
print("Option Price is:", round(option_price, 2))   # Round Price to 2 Decimal Places
