#Importing required libraries
import tkinter
from tkinter import *
from tkinter import messagebox
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import time
import copy
from bs4 import BeautifulSoup
import requests
from licensing import *
import yfinance as yf
import fxcmpy
#import window1 if running windows2and3 file directly


########################## WINDOW 3 #################################


def window3():
 win3 = tkinter.Tk()
 win3.geometry("770x500")
 win3.resizable (False, False)
 win3.iconbitmap('chart.ico')
 win3.title (" Ticker Analysis Screen ")

 def indicator_analysis():
     print(indicator_ana_val.get())

 def ticker_graph():
    def CAGR(DF):
        #function to calculate the Cumulative Annual Growth Rate of a trading strategy
        df = DF.copy()
        df["cum_return"] = (1 + df["mon_ret"]).cumprod()
        n = len(df)/12
        CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
        return CAGR

    def volatility(DF):
        #function to calculate annualized volatility of a trading strategy
        df = DF.copy()
        vol = df["mon_ret"].std() * np.sqrt(12)
        return vol

    def sharpe(DF,rf):
        #function to calculate sharpe ratio ; rf is the risk free rate
        df = DF.copy()
        sr = (CAGR(df) - rf)/volatility(df)
        return sr
        
    def max_dd(DF):
        #function to calculate max drawdown
        df = DF.copy()
        df["cum_return"] = (1 + df["mon_ret"]).cumprod()
        df["cum_roll_max"] = df["cum_return"].cummax()
        df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
        df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
        max_dd = df["drawdown_pct"].max()
        return max_dd

    #Download historical data (monthly) for DJI constituent stocks
    tickers = [access_value]
    #Directory with ohlc value for each stock
    ohlc_mon = {}             
    start = dt.datetime.today()-dt.timedelta(1980)
    end = dt.datetime.today()

    #Looping over tickers and creating a dataframe with close prices
    for ticker in tickers:
        ohlc_mon[ticker] = yf.download(ticker,start,end,interval='1mo')
        ohlc_mon[ticker].dropna(inplace=True,how="all")

    #Redefine tickers variable after removing any tickers with corrupted data
    tickers = ohlc_mon.keys() 

    #Backtesting
    #Calculating monthly return for each stock and consolidating return info by stock in a separate dataframe
    ohlc_dict = copy.deepcopy(ohlc_mon)
    return_df = pd.DataFrame()
    for ticker in tickers:
        print("calculating monthly return for ",ticker)
        ohlc_dict[ticker]["mon_ret"] = ohlc_dict[ticker]["Adj Close"].pct_change()
        return_df[ticker] = ohlc_dict[ticker]["mon_ret"]
    return_df.dropna(inplace=True)

    #Function to calculate portfolio return iteratively
    def pflio(DF,m,x):
        """Returns cumulative portfolio return
        DF = dataframe with monthly return info for all stocks
        m = number of stock in the portfolio
        x = number of underperforming stocks to be removed from portfolio monthly"""
        df = DF.copy()
        portfolio = []
        monthly_ret = [0]
        for i in range(len(df)):
            if len(portfolio) > 0:
                monthly_ret.append(df[portfolio].iloc[i,:].mean())
                bad_stocks = df[portfolio].iloc[i,:].sort_values(ascending=True)[:x].index.values.tolist()
                portfolio = [t for t in portfolio if t not in bad_stocks]
            fill = m - len(portfolio)
            new_picks = df.iloc[i,:].sort_values(ascending=False)[:fill].index.values.tolist()
            portfolio = portfolio + new_picks
            print(portfolio)
        monthly_ret_df = pd.DataFrame(np.array(monthly_ret),columns=["mon_ret"])
        return monthly_ret_df

    #calculating overall strategy's KPIs
    CAGR(pflio(return_df,6,3))
    sharpe(pflio(return_df,6,3),0.025)
    max_dd(pflio(return_df,6,3)) 

    #calculating KPIs for Index buy and hold strategy over the same period
    DJI = yf.download("^DJI",dt.date.today()-dt.timedelta(1980),dt.date.today(),interval='1mo')
    DJI["mon_ret"] = DJI["Adj Close"].pct_change().fillna(0)
    CAGR(DJI)
    sharpe(DJI,0.025)
    max_dd(DJI)

    #visualization
    fig, ax = plt.subplots()
    plt.plot((1+pflio(return_df,6,3)).cumprod())
    plt.plot((1+DJI["mon_ret"].reset_index(drop=True)).cumprod())
    plt.title("Graph of Ticker")
    plt.ylabel("Cumulative return")
    plt.xlabel("Months")
    ax.legend(["Portfolio rebalancing strategy","Buy and hold strategy"])
    plt.show()

 #Title
 title_label1 = Label(win3, text = "Trading Analysis and Automated Trading", height = 3, font = "Arial 18 bold")
 title_label1.grid(column = 1, row = 1, sticky = E)
 
 #Ticker output
 ticker_output_label = Label(win3, text = " Ticker", height = 3, font = "Arial 13")
 ticker_name_entry = Entry(win3, width = 18, relief = GROOVE, exportselection= 0)
 ticker_output_label.grid(column = 0, row = 4, sticky = W)
 ticker_name_entry.grid(column = 1, row = 4, sticky = W, ipadx = 25, ipady = 3.7)
 access_value = ticker_value.get()
 print(access_value)
 ticker_name_entry.insert(0, access_value)
 
 #Indicator analysis
 indicator_analysis_label = Label(win3, text = " Indicator Analysis ", height = 3, font = "Arial 13")
 indicator_analysis_entry = Entry(win3, width = 18, relief = GROOVE)
 indicator_analysis_label.grid(column = 0, row = 5, sticky = W)
 indicator_analysis_entry.grid(column = 1, row = 5, sticky = W, ipadx = 25, ipady = 3.7)
 indicator_analysis_entry.insert(1, '65m')

 #Graph access
 graph_button = Button(win3, text = "Graph of Ticker", width = 30, height = 1, command = ticker_graph, font = "Arial 12")
 graph_button.place(x = 250, y = 230)
 
 win3.mainloop()


########################## WINDOW 2 ##################################


#Window 2
win2 = tkinter.Tk()
win2.geometry("670x500")
win2.resizable (False, False)
win2.iconbitmap('chart.ico')
win2.title (" Trading Screen ")

top_indicators= ["SMA", "EMA", "MACD", "Bollinger Bands", "RSI", "ATR", "ADX"]

#Defining vars
ticker_value = tkinter.StringVar()
trade_slot_value = tkinter.IntVar(win2)

#Opening next page
def next_page3():
   window3() 

def clear_ticker_value():
    ticker_choice_entry.delete(0, 'end')
    value_entry.delete(0, 'end')

#Ticker value calculation and displaying
def ticker_val():
    ticker = ticker_value.get()
    url = "https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch".format(ticker, ticker)
    headers = {"User-Agent" : "Chrome/97.0.4692.99"}
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    price = soup.find_all('tr', {'class' : 'Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($seperatorColor) H(36px)'})[-11].text
    replace = price.replace('Ask', '')
    without_x = replace
    head, sep, tail = without_x.partition('x')
    print(ticker, ":", head)
    value_entry.insert(0, head)

#Display list on selection
def top_tickers_list():
    url = "https://finance.yahoo.com/most-active"
    headers = {"User-Agent" : "Chrome/97.0.4692.99"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    tick1 = soup.find_all('a', {'class' : 'Fw(600) C($linkColor)'})[0].text
    tick2 = soup.find_all('a', {'class' : 'Fw(600) C($linkColor)'})[1].text
    tick3 = soup.find_all('a', {'class' : 'Fw(600) C($linkColor)'})[2].text
    tick4 = soup.find_all('a', {'class' : 'Fw(600) C($linkColor)'})[3].text
    tick5 = soup.find_all('a', {'class' : 'Fw(600) C($linkColor)'})[4].text
    tick6 = soup.find_all('a', {'class' : 'Fw(600) C($linkColor)'})[5].text
    tick7 = soup.find_all('a', {'class' : 'Fw(600) C($linkColor)'})[6].text
    tick8 = soup.find_all('a', {'class' : 'Fw(600) C($linkColor)'})[7].text
    tick9 = soup.find_all('a', {'class' : 'Fw(600) C($linkColor)'})[8].text
    tick10 = soup.find_all('a', {'class' : 'Fw(600) C($linkColor)'})[9].text
    print(tick1, tick2, tick3, tick4, tick5, tick6, tick7, tick8, tick9, tick10)

    ticker_screen = tkinter.Tk()
    ticker_screen.geometry ("300x220")
    ticker_screen.title ("Top 10 Tickers Screen")
    ticker_label_menu = Label(ticker_screen, height = 2, text = "Most Active Tickers List")
    ticker_label_menu.pack()
    menu = Listbox(ticker_screen, bd = 0, justify = CENTER)
    menu.insert(1, tick1)
    menu.insert(2, tick2)
    menu.insert(3, tick3)
    menu.insert(4, tick4)
    menu.insert(5, tick5)
    menu.insert(6, tick6)
    menu.insert(7, tick7)
    menu.insert(8, tick8)
    menu.insert(9, tick9)
    menu.insert(10, tick10)
    menu.pack()
    ticker_screen.mainloop()
   
#Indicator instructions
def indicator_steps(self):
   tickers = ticker_value.get()
   # importing stock price
   df_tkr = pdr.get_data_yahoo(tickers, start="2021-01-01", end="2022-01-01") #insert your time slot
   df_tkr.head()
   fig = plt.figure(figsize=(10, 10))
   ax = plt.subplot()
   stocks = StockDataFrame.retype(df_tkr[["Open", "Close", "High", "Low", "Volume"]])

   ############# SMA ###################  
   if (variable_options.get() == "SMA"):
      print("SMA is selected")
      
      plt.title("Simple Moving Average")
      plt.plot(stocks["close_5_sma"], color="blue", label="SMA 5-day")
      plt.plot(stocks["close_10_sma"], color="green", label="SMA 10-day")
      plt.plot(df_tkr.Close, color="red", label="Close prices")
      plt.legend(loc="upper left")
      plt.show()
      
   ############# EMA ###################
   elif (variable_options.get() == "EMA"):
      print("EMA is selected")
      plt.title("Exponential Moving Average")
      plt.plot(stocks["close_10_sma"], color="blue", label="SMA 10-day")
      plt.plot(stocks["close_10_ema"], color="green", label="EMA 10-day")
      plt.plot(df_tkr.Close, color="red", label="Close prices")
      plt.legend(loc="upper left")
      plt.show()
      
   ############## MACD ###################
   elif (variable_options.get() == "MACD"):
      print("MACD is selected")
      plt.title("Moving Average Convergence Divergence")
      plt.plot(stocks["macd"], color="blue", label="MACD Line")
      plt.plot(stocks["macds"], color="green", label="Signal Line")
      plt.legend(loc="upper left")
      plt.show()
      
   ############## Bollinger Bands ###################
   elif (variable_options.get() == "Bollinger Bands"):
      print("Bollinger Bands is selected")
      plt.title("Bollinger Bands")
      plt.plot(stocks["close_20_sma"], color="red", label="SMA 20-day")
      plt.plot (stocks["boll_ub"], color="blue", label="Upper Bollinger Band")
      plt.plot (stocks["boll_lb"], color="green", label="Lower Bollinger Band")
      plt.legend(loc="upper left")
      plt.show()
      
   ############# RSI ###################
   elif (variable_options.get() == "RSI"):
      print("RSI is selected")
      plt.title("Relative Strength Index")
      plt.plot (stocks["rsi_6"], color="blue", label="RSI 6-day")
      plt.plot (stocks["rsi_12"], color="green", label="RSI 12-day")
      plt.plot(df_tkr.Close, color="red", label="Close price")
      plt.legend(loc="upper left")
      plt.show()
      
   ############# ATR ###################
   elif (variable_options.get() == "ATR"):
      print("ATR is selected")
      plt.title("Average True Range")
      plt.plot (stocks["tr"], color="blue", label="TR")
      plt.plot (stocks["atr"], color="green", label="ATR")
      plt.legend(loc="upper left")
      plt.show()
      
   ############# ADX ###################
   elif (variable_options.get() == "ADX"):
      print("ADX is selected")
      plt.title("Average Directional Index")
      plt.plot (stocks["atr"], color="blue", label="ATR")
      plt.plot (stocks["dx"], color="red", label="DX")
      plt.plot (stocks["adx"], color="green", label="ADX")
      plt.legend(loc="upper left")
      plt.show()

def trade_entered_slots():
    #Slot window
    slot_screen = tkinter.Tk()
    slot_screen.geometry ("670x500")
    slot_screen.resizable (False, False)
    slot_screen.iconbitmap('chart.ico')
    slot_screen.title ("Trade Slot Screen")

    #Token and connection (FXCM)
    con = fxcmpy.fxcmpy(config_file='fxcm.cfg', server='demo') #add your fxcm token file in the same folder

    #Getting acc data
    print("Account data: ", con.get_accounts().T)
    
    #Buy and Sell functions
    def buy_trade():
        print("BUY SLOT")
        buying = con.create_market_buy_order('USD/JPY', 200)
        print("BUY: ", buying)

    def sell_trade():
        print("SELL SLOT")
        selling = con.create_market_sell_order('EUR/USD', 100)
        print("SELL: ", selling)
    
    con.close()
        
    #Ticker and indicator entry
    ticker1_output_label = Label(slot_screen, text = " Ticker ", height = 3, font = "Arial 13")
    ticker1_name_entry = Entry(slot_screen, width = 18, relief = GROOVE, exportselection= 0)
    access_value1 = ticker_value.get()
    print(access_value1)
    ticker1_name_entry.insert(0, access_value1)
    ticker1_output_label.grid(column = 0, row = 0, sticky = W)
    ticker1_name_entry.grid(column = 1, row = 0, sticky = W, ipadx = 25, ipady = 3.7)

    indicator_output_label = Label(slot_screen, text = " Indicator ", height = 3, font = "Arial 13")
    indicator_name_entry = Entry(slot_screen, width = 18, relief = GROOVE, exportselection= 0)
    indi_val = variable_options.get()
    indicator_name_entry.insert(0, indi_val)   
    indicator_output_label.grid(column = 0, row = 1, sticky = W)
    indicator_name_entry.grid(column = 1, row = 1, sticky = W)

    value_slots = Label(slot_screen, text = " Number of slots ", height = 3, font = "Arial 13")
    value_slots_entry = Entry(slot_screen, width = 18, relief = GROOVE, exportselection= 0)
    slot_val = trade_slot_value.get()
    value_slots_entry.insert(0, slot_val) 
    value_slots.grid(column = 0, row = 2, sticky = W)
    value_slots_entry.grid(column = 1, row = 2, sticky = W)
    
    #Buy and sell options
    buy_button = Button(slot_screen, text = "Buy", width = 10, height = 1, font = "Arial 12", command = buy_trade)
    buy_button.grid(column = 0, row = 3, sticky = W)
    sell_button = Button(slot_screen, text = "Sell", width = 10, height = 1, font = "Arial 12", command = sell_trade)
    sell_button.grid(column = 1, row = 3, sticky = W)

#Title
title_label = Label(win2, text = "Trading Analysis and Automated Trading", height = 3, font = "Arial 18 bold")
title_label.grid(column = 1, row = 1, sticky = E)

#Ticker choice
ticker_choice_label = Label(win2, text = " Ticker", height = 3, font = "Arial 13")
ticker_choice_entry = Entry(win2, width = 18, relief = GROOVE, textvariable = ticker_value)
ticker_bitmap = Button(win2, text = "Hourglass", bitmap = "hourglass", height = 27, width = 18, bd = 0, command = ticker_val)
ticker_choice_label.grid(column = 0, row = 4, sticky = W)
ticker_choice_entry.grid(column = 1, row = 4, sticky = W, ipadx = 25, ipady = 3.7)
ticker_bitmap.place(x = 255, y = 110)

#Value displaying
value_label = Label(win2, text = "Value", height = 3, font = "Arial 13")
value_entry = Entry (win2, width = 18, relief = GROOVE)
value_label.place(x = 300, y = 93)
value_entry.place(x = 370, y = 110, width = 155, height = 28)

#Clear button
clear_ticker_value = Button(win2, text = "Clear", width = 10, height = 1, command = clear_ticker_value, font = "Arial 12")
clear_ticker_value.grid(column = 1, row = 5, sticky = W)

#Indicators menu
indicator_menu_label = Label(win2, text = " Indicator", height = 3, font = "Arial 13")
indicator_menu_label.grid(column = 0, row = 6, sticky = W)
variable_options = StringVar(win2)
variable_options.set(top_indicators[0])
options_indicator = OptionMenu(win2, variable_options, *top_indicators, command = indicator_steps)
options_indicator.config(width = 18, height = 1)
options_indicator.grid(column = 1, row = 6, sticky = W)

#Auto trade slot
trade_slot_label = Label(win2, text = " Trade Slot ", height = 3, font = "Arial 13")
trade_slot_entry = Entry(win2, width = 18, relief = GROOVE, textvariable = trade_slot_value)
trade_slot_bitmap = Button(win2, text = "Hourglass", bitmap = "hourglass", height = 27, width = 18, bd = 0, command = trade_entered_slots)
trade_slot_label.grid(column = 0, row = 7, sticky = W)
trade_slot_entry.grid(column = 1, row = 7, sticky = W, ipadx = 25, ipady = 3.7)
trade_slot_bitmap.place(x = 255, y = 268)

#Analysis trade (Window 3)
analysis_trade_button = Button (win2, text = "Analysis Trade", width = 30, height = 1, command = next_page3, font = "Arial 12")
analysis_trade_button.place(x = 170, y = 320)

#Top 10
top_10_button = Button (win2, text = "Top 10", width = 15, height = 1, command = top_tickers_list, font = "Arial 12")
top_10_button.place(x = 230, y = 370)

win2.mainloop()
input()
