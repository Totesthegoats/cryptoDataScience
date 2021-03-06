'''
Created on 15 Feb 2022
@author: TotesMcGoats
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.optimize import curve_fit
import nasdaqdatalink

# This data was gotten on https://data.nasdaq.com/, you need an account to download it, but you have 50 free API calls per day and unlimited if you sign up, which is free.
data = yf.download('TSLA').reset_index()

# Plot the close price of the AAPL
#data['Adj Close'].plot()
#plt.show()

raw_data = data[["Date", "Close"]].copy()

#
raw_data['Date'] = pd.to_datetime(raw_data['Date']) # Ensure that the date is in datetime or graphs might look funny
raw_data = raw_data[raw_data["Close"] > 0] # Drop all 0 values as they will fuck up the regression bands

# this is your log fucyion,
def logFunc(x,a,b):
    return a*np.log(x) + b

# getting your x and y data from the dataframe
xdata = np.array([x+1 for x in range(len(raw_data))])
ydata = np.log(raw_data["Close"])
#plt.plot(ydata)
#plt.show()
# here we ar fitting the curve, you can use 2 data points however I wasn't able to get a graph that looked as good with just 2 points.
popt, pcov = curve_fit(logFunc, xdata, ydata, p0 = [10,10], maxfev=100000000) # p0 is just a guess, doesn't matter as far as I know

# This is our fitted data, remember we will need to get the ex of it to graph it
fittedYData = logFunc(xdata, popt[0], popt[1])

# Dark background looks nice
plt.style.use("dark_background")
# Plot in a with long Y axis
plt.semilogy(raw_data["Date"], raw_data["Close"])

# Draw the rainbow bands
for i in range(-2,6):
    raw_data[f"fitted_data{i}"] = np.exp(fittedYData + i*.455)
    plt.plot(raw_data["Date"], np.exp(fittedYData + i*.455))
    plt.ylim(bottom=3)
    #You can use the below plot fill between rather than the above line plot, I prefer the line graph
    #plt.fill_between(raw_data["Date"], np.exp(fittedYData + i*.45 -1), np.exp(fittedYData + i*.45), alpha=0.4)
#
# # Back Testing
# df = raw_data
# # Change the DCA time frame here, daily = df[::1], weekly = [::7], biweekly = [::14], monthly = [::30], yearly = df[::365]
# monthly = df[::30].reset_index()
# # Change the date you start to DCA here
# monthly = monthly[monthly['Date'] > '2019-01-01']
# # Change your buy amount here
# buyAmount = 100
# totalDCA = 0
# totalRCA = 0
# amount_invested_DCA = 0
# amount_invested_RCA = 0
# fibs = {6:0, 5:0.1, 4:0.2, 3:0.3, 2:0.5, 1:0.8, 0:1.3,-1:2.1,-2:3.4}
# originalRCA = {6:0, 5:0.1, 4:0.2, 3:0.35, 2:0.5, 1:0.75, 0:1,-1:2.5,-2:3}
# # Choose what type of weightings you want to RCA with
# weighted = fibs
# # This loop calculates what rainbow regression bands each data point for your DCA falls between.
# for x in range(0, len(monthly)):
#     # if below the first band the buy buyAmount*3.4 and so on for each successive line
#     if monthly.Value.iloc[x] < monthly["fitted_data-2"].iloc[x]:
#         print("Bitcoin is below $", monthly["fitted_data-1"].iloc[x], " therefore our multiplier is ", weighted[-2])
#         totalDCA = totalDCA + buyAmount/monthly.Value.iloc[x]
#         totalRCA = totalRCA + buyAmount * weighted[-2] / monthly.Value.iloc[x]
#         amount_invested_RCA = amount_invested_RCA + buyAmount * weighted[-2]
#         amount_invested_DCA = amount_invested_DCA + buyAmount
#
#     elif monthly.Value.iloc[x] > monthly["fitted_data-2"].iloc[x] and monthly.Value.iloc[x] < monthly["fitted_data-1"].iloc[x]:
#         print("Bitcoin is below $", monthly["fitted_data-1"].iloc[x], " therefore our multiplier is ", weighted[-1])
#         totalDCA = totalDCA + buyAmount/monthly.Value.iloc[x]
#         totalRCA = totalRCA + buyAmount * weighted[-1] / monthly.Value.iloc[x]
#         amount_invested_RCA = amount_invested_RCA + buyAmount * weighted[-1]
#         amount_invested_DCA = amount_invested_DCA + buyAmount
#
#     elif monthly.Value.iloc[x] > monthly["fitted_data-1"].iloc[x] and monthly.Value.iloc[x] < monthly["fitted_data0"].iloc[x]:
#         print("Bitcoins price falls between $", monthly["fitted_data-1"].iloc[x], "and $", monthly["fitted_data0"].iloc[x], " therefore our multiplier is ", weighted[0])
#         totalDCA = totalDCA + buyAmount/monthly.Value.iloc[x]
#         totalRCA = totalRCA + buyAmount * weighted[0] / monthly.Value.iloc[x]
#         amount_invested_RCA = amount_invested_RCA + buyAmount * weighted[0]
#         amount_invested_DCA = amount_invested_DCA + buyAmount
#
#
#     elif monthly.Value.iloc[x] > monthly["fitted_data0"].iloc[x] and monthly.Value.iloc[x] < monthly["fitted_data1"].iloc[x]:
#         print("Bitcoins price falls between $", monthly["fitted_data0"].iloc[x], "and $", monthly["fitted_data1"].iloc[x], " therefore our multiplier is ", weighted[1])
#         totalDCA = totalDCA + buyAmount/monthly.Value.iloc[x]
#         totalRCA = totalRCA + buyAmount * weighted[1] / monthly.Value.iloc[x]
#         amount_invested_RCA = amount_invested_RCA + buyAmount * weighted[1]
#         amount_invested_DCA = amount_invested_DCA + buyAmount
#
#     elif monthly.Value.iloc[x] > monthly["fitted_data1"].iloc[x] and monthly.Value.iloc[x] < monthly["fitted_data2"].iloc[x]:
#         print("Bitcoins price falls between $", monthly["fitted_data1"].iloc[x], "and $", monthly["fitted_data2"].iloc[x], " therefore our multiplier is ", weighted[1])
#         totalDCA = totalDCA + buyAmount/monthly.Value.iloc[x]
#         totalRCA = totalRCA + buyAmount * weighted[1] / monthly.Value.iloc[x]
#         amount_invested_RCA = amount_invested_RCA + buyAmount * weighted[2]
#         amount_invested_DCA = amount_invested_DCA + buyAmount
#
#     elif monthly.Value.iloc[x] > monthly["fitted_data2"].iloc[x] and monthly.Value.iloc[x] < monthly["fitted_data3"].iloc[x]:
#         print("Bitcoins price falls between $", monthly["fitted_data2"].iloc[x], "and $", monthly["fitted_data3"].iloc[x], " therefore our multiplier is ", weighted[2])
#         totalDCA = totalDCA + buyAmount/monthly.Value.iloc[x]
#         totalRCA = totalRCA + buyAmount * weighted[2] / monthly.Value.iloc[x]
#         amount_invested_RCA = amount_invested_RCA + buyAmount * weighted[2]
#         amount_invested_DCA = amount_invested_DCA + buyAmount
#
#     elif monthly.Value.iloc[x] > monthly["fitted_data3"].iloc[x] and monthly.Value.iloc[x] < monthly["fitted_data4"].iloc[x]:
#         print("Bitcoins price falls between $", monthly["fitted_data3"].iloc[x], "and $", monthly["fitted_data4"].iloc[x], " therefore our multiplier is ", weighted[3])
#         totalDCA = totalDCA + buyAmount/monthly.Value.iloc[x]
#         totalRCA = totalRCA + buyAmount * weighted[3] / monthly.Value.iloc[x]
#         amount_invested_RCA = amount_invested_RCA + buyAmount * weighted[3]
#         amount_invested_DCA = amount_invested_DCA + buyAmount
#
#     elif monthly.Value.iloc[x] > monthly["fitted_data4"].iloc[x] and monthly.Value.iloc[x] < monthly["fitted_data5"].iloc[x]:
#         print("Bitcoins price falls between $", monthly["fitted_data4"].iloc[x], "and $", monthly["fitted_data5"].iloc[x], " therefore our multiplier is ", weighted[4])
#         totalDCA = totalDCA + buyAmount/monthly.Value.iloc[x]
#         totalRCA = totalRCA + buyAmount * weighted[4] / monthly.Value.iloc[x]
#         amount_invested_RCA = amount_invested_RCA + buyAmount * weighted[4]
#         amount_invested_DCA = amount_invested_DCA + buyAmount
#
#     else:
#         print("Don't buy bitcoin")
#         totalDCA = totalDCA + buyAmount/monthly.Value.iloc[x]
#         totalRCA = totalRCA + buyAmount * weighted[5] / monthly.Value.iloc[x]
#         amount_invested_RCA = amount_invested_RCA + buyAmount * weighted[5]
#         amount_invested_DCA = amount_invested_DCA + buyAmount
#
# # This plots the locations of your buy points.
# plt.scatter(monthly["Date"],monthly["Value"], c="red")
#
#
# print("Total value RCA ", totalRCA)
# print("Total value DCA ", totalDCA)
# print(amount_invested_RCA)
# print(amount_invested_DCA)

plt.show()