'''Trading bot that gathers information and acts on that information'''

import pandas as pd
import matplotlib as mpl 
import numpy as np
import quandl as q

q.ApiConfig.api_key = "8fLze8ZvBkogbkyRi8Cc"

msft_data = q.get("EOD/MSFT", start_date="2010-01-10", end_date="2019-01-01")
print(msft_data.head())
print(msft_data.describe())
msft_data.resample("M").mean()

daily_close = msft_data[["Adj_Close"]]
daily_return = daily_close.pct_change()
daily_return.fillna(0, inplace=True)
print(daily_return)

mdata = msft_data.resample("M").apply(lambda x: x[-1])
monthly_return = mdata.pct_change()

adj_pricesadj_price = msft_data["Adj_Close"]
mav = adj_pricesadj_price.rolling(window=50).mean()
print(mav[-10:])

adj_pricesadj_price.plot()
mav.plot()

short_lb = 50
long_lb = 120
signal_df = pd.DataFrame(index=msft_data.index)signal_df['signal'] = 0.0
signal_df["short_mav"] = msft_data["Adj_Close"].rolling(windows=short_lb,min_periods=1, center=False).mean()
signal_df["long_mav"] = msft_data["Adj_Close"].rolling(windows=long_lb,min_periods=1, center=False).mean()
signal_df["signal"]["short_lb"] = np.where(signal_df["short_mav"][short_lb]>signal_df["long_mav"]["short_lb"], 1.0, 0.0)
signal_df["positions"] = signal_df["signal"].diff()signal_df[signal_df["positions"] == - 1.0]

fig = plt.figure()
plt1 = fig.add_subplot(111, ylabel="Price in $")
msft_data["Adj_Close"].plot(ax=plt1, color="r", lw=2.)
signal_df[["short_mav", "long_mav"]].plot(ax=plt1, lw=2, figsize=(12, 8))
plt1.plot(signal_df.loc[signal_df.positions == -1.0].index, signal_df.short_mav[signal_df.positions == -1.0], 'v')
plt1.lot(signal_df.loc[signal_df.positions == 1.0].index, signal_df.short_mav[signal_df.positions == 1.0], '^', markersize=10, color="m")