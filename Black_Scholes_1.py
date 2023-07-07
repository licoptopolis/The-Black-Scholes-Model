# Black Scholes Model
# Assumptions for this calculator:
# European options that can only be exercised at expiration
# No dividends to be paid out during the options lifespan
# The return on the underlying are normally distributed

# variable Sample
    # R = 0.01        # Interest Rate
    # S = 30          # underlying Price
    # K = 10          # Strike Price
    # T = 252/365     # Time to Maturity
    # sigma = 0.30    # Volatility

import numpy as np
from scipy.stats import norm

def inputs():
    R = None
    while R is None:
        try:
            R = float(input("Interest Rate: "))
        except ValueError:
            print("\033[31mInvalid input. Please enter a valid value.\033[m")
    S = None
    while S is None:
        try:
            S = float(input("Underlying Price: "))
        except ValueError:
            print("\033[31mInvalid input. Please enter a valid value.\033[m")
    K = None
    while K is None:
        try:
            K = float(input("Strike Price: "))
        except ValueError:
            print("\033[31mInvalid input. Please enter a valid value.\033[m")
    T = None
    while T is None:
        try:
            T = eval(input("Time to Maturity: "))
        except (NameError, SyntaxError):
            print("\033[31mInvalid input. Please enter a valid value.\033[m")
    sigma = None
    while sigma is None:
        try:
            sigma = float(input("Volatility: "))
        except ValueError:
            print("\033[31mInvalid input. Please enter a valid value.\033[m")
    option_selection = None
    while option_selection is None:
        option_selection = input("Option Type - Call or Put (C/P): ").upper()
        if option_selection not in ["C", "P"]:
            print("\033[31mInvalid input. Please enter 'C' for call option or 'P' for put option.\033[m")
    return R, S, K, T, sigma, option_selection

def black_scholes(R,S,K,T, sigma, type="C" or "P"):
    "Calulate Black Scholes option price for call or put"
    d1 = (np.log(S/K) + (R + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if type == "C":
        price = S * norm.cdf(d1) - K * np.exp(-R * T) * norm.cdf(d2)
    elif type == "P":
        price = K * np.exp(-R * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Choose 'C' for call or 'P' for put.")
    return price

R, S, K, T, sigma, option_selection = inputs() # Calling Input Function
option_price = black_scholes(R, S, K, T, sigma, type=option_selection)
print("Option price is:", round(option_price, 2))