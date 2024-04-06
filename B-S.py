'''
Black Scholes Model with yFinance API
Assumptions for this model:
- European options that can only be exercised at expiration
- No dividends to be paid out during the options' lifespan
- The return on the underlying are normally distributed
'''
'''
Variables:
    R                # Interest Rate
    S                # underlying Price
    K                # Strike Price
    T = 000/365      # Time to Maturity
    sigma            # Volatility
'''
# Importing libraries
import numpy as np
import yfinance as yf
from scipy.stats import norm

# Defining user inputs
def symbol_inputs():
    while True:
        symbol = input('Enter stock/ticker: ')
        try:
            stock_data = yf.download(symbol, progress=False)
            if stock_data.empty:
                print("No data found, enter valid ticker symbol: \n")
            else:
                last_adj_close = stock_data['Adj Close'].iloc[-1]
                formatted_last_adj_close = "{:.2f}".format(last_adj_close)
                print(f"Last adjusted close price: {formatted_last_adj_close} \n")
                return symbol, stock_data
        except Exception as e:
            print("An error has occurred, enter a valid ticker symbol")

def variables(stock_data):
    s = (round(stock_data['Adj Close'].iloc[-1], 2))

    data1 = round(yf.download("^TNX", progress=False)['Adj Close'].iloc[-1], 2)
    r = (round(data1 / 100, 2))

    #print("Please enter the strike price below:", flush=True)
    k = None
    while k is None:
        try:
            k = float(input("Strike Price: "))
        except ValueError:
            print('Invalid input, please enter a valid strike price value ')
    print('')
    t = None
    while t is None:
        try:
            t = float(eval(input('time to maturity (displayed as 000/365): ')))
        except (NameError, SyntaxError):
            print('Invalid input, please enter a valid value')
    print('')
    data2 = round(yf.download("^VIX", progress=False)['Adj Close'].iloc[-1], 2)
    sigma = (round(data2 / 10, 2))

    #print('Please enter "C" for Call or "P" for Put below: ', flush=True)
    option_type = None
    while option_type is None:
        option_type = input('Call or Put? "C" for Call and "P" for Put: ').upper()
        if option_type not in ["C", "P"]:
            print('Invalid input, please enter a valid value')

    return r, s, k, t, sigma, option_type

#Black Scholes Model
def black_scholes(r: float, s: float, k: float, t: float, sigma: float, option_type: str) -> float:
    """Calculate option price for calls or puts using the Black-Scholes formula."""
    d1 = (np.log(s / k) + (r + sigma ** 2 / 2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)

    if option_type == "C":
        price = s * norm.cdf(d1) - k * np.exp(-r * t) * norm.cdf(d2)
    elif option_type == "P":
        price = k * np.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Choose 'C' for call or 'P' for put.")
    # Debug print statement (optional, remove or comment out for production use)
    # print('debug', f"d1: {d1}, d2: {d2}, Call Price if 'C': {s * norm.cdf(d1) - k * np.exp(-r * t) * norm.cdf(d2)}, Put Price if 'P': {k * np.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)}")
    return price

symbol, stock_data = symbol_inputs()
r, s, k, t, sigma, option_type = variables(stock_data)
option_price = black_scholes(r, s, k, t, sigma, option_type)
print('')
print('Option Price is: ', round(option_price, 2))