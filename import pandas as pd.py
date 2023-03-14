import pandas as pd

# Load the Bitcoin price data from a CSV file
btc_data = pd.read_csv('bitcoin_price_data.csv')

# set initial capital and holding values
capital = 10000
holdings = 0
buy_price = 0
stop_loss = 0

# set the buy and sell thresholds
buy_threshold = 0.01
sell_threshold = 0.1

# keep track of capital after each trade
capital_history = [capital]

# keep track of whether the previous price has decreased
prev_decreased = False

# iterate through each row in the data
for i, row in btc_data.iterrows():
    # get the current price and volume
    price = row['Close']
    volume = row['Volume_(BTC)']

    # skip this iteration if price is NaN
    if pd.isna(price):
        continue

    # calculate the change in price since the last time step
    if i > 0:
        price_change = price - btc_data.loc[i-1, 'Close']
    else:
        price_change = 0

    # check if we should buy
    if prev_decreased and price_change < -buy_threshold and holdings == 0 and volume > btc_data.loc[i-1, 'Volume_(BTC)']:
        # calculate the amount to buy
        amount = capital / price
        # update the holdings and buy price
        holdings = amount
        buy_price = price
        # update the stop loss
        stop_loss = price * 0.995
        # update the previous decreased flag
        prev_decreased = False
        # update the capital
        capital -= amount * price
        # print the buy message
        print(f"Buy {amount:.6f} BTC at {price:.2f}. Capital: {capital:.2f}")

    # check if we should sell
    elif price_change > sell_threshold and holdings > 0:
        # calculate the amount to sell
        amount = holdings
        # update the holdings and buy price
        holdings = 0
        buy_price = 0
        # update the capital
        capital += amount * price
        # calculate the profit
        profit = (amount * price) - (amount * buy_price)
        # update the capital history
        capital_history.append(capital)
        # print the sell message and profit
        print(f"Sell {amount:.6f} BTC at {price:.2f}. Profit: {profit:.2f}. Capital: {capital:.2f}")
        # check if capital has reached 0
        if capital <= 0:
            print("Capital has reached 0. Stopping script.")
            break

    # check if we should cut losses
    elif price < stop_loss and holdings > 0:
        # calculate the amount to sell
        amount = holdings
        # update the holdings and buy price
        holdings = 0
        buy_price = 0
        # update the capital
        capital += amount * price
        # calculate the profit
        profit = (amount * price) - (amount * buy_price)
        # update the capital history
        capital_history.append(capital)
        # print the sell message and profit
        print(f"Sell {amount:.6f} BTC at {price:.2f} due to stop loss. Loss: {profit:.2f}. Capital: {capital:.2f}")
        # check if capital has reached 0
        if capital <= 0:
            print("Capital has reached 0. Stopping script")


