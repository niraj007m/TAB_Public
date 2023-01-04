"""

Trading Analysis and Automated Trading model
Company name: Vormir Infotech LLP
Developed by: Simran Naryani



Concepts used:

---------------- DEFINITIONS ----------------

Moving average- Smooths the price data to form a trend following indicator.

Simple Moving Average(SMA)- Formed by computing the average price of a security over a specific number of periods.

Exponential Moving Average(EMA)- Reduces the lag by applying more weight to recent prices.

Moving Average Convergence/Divergence(MACD)- Turns two trend-following indicators/moving averages, into a momentum oscillator.

Bollinger Bands(BB)- Volatility bands placed above and below a moving average.

Relative Strength Index(RSI)- Momentum oscillator that measures the speed and change of price movements.

Average True Range(ATR)- Indicator that measures volatility.

+DI, -DI- Derived from smoothed averages of these differences and measure trend direction over time. Collectively referred as Directional Movement Indicator(DMI).

Average Directional Index(ADX)- Derived from the smoothed averages of the difference between +DI and -DI. Measures strength of the trend over time.


---------------- INDICATOR FORMULAS ----------------

Calculating SMA:
SMA = (Sum(Price, n)) / n
Where, n = Time Period

Calculating EMA:
SMA = (Sum(Price, n)) / n
Multiplier = {2 / (total observations + 1)}
EMA = [Closing price x Multiplier] + [Previous day EMA x (1 - Multiplier)

Calculating MACD:
MACD Line = 12 Period EMA − 26 Period EMA
Signal Line = 9 Period EMA of MACD Line

Calculating BB:
SMA = (Sum(Price, n)) / n
Middle Band = 20 Period SMA
Upper Band = 20 Period SMA + (20 Period standard deviation of price x 2) 
Lower Band = 20 Period SMA - (20 Period standard deviation of price x 2)
Where, n = Time Period

Calculating RSI:
Average Gain = [(previous Average Gain) x 13 + current Gain] / 14
Average Loss = [(previous Average Loss) x 13 + current Loss] / 14
Where, 14 = default period

Calculating ATR:
TR = high - low
Current ATR = [(Prior ATR x 13) + Current TR] / 14
Where, 14 = default period

Calculating ADX:
TR = high - low
Current ATR = [(Prior ATR x 13) + Current TR] / 14
+DI = (Smoothed + directional movement ÷ ATR) x 100
-DI = (Smoothed - directional movement ÷ ATR) x 100
DX = ((+DI – -DI) ÷ (+DI + -DI)) x 100
ADX = ((Prior ADX x 13) + Current ADX) ÷ 14
Where, 14 = default period


---------------- LIBRARIES USED ----------------

Tkinter: Tkinter is the standard GUI library used. Python when combined with Tkinter provided a faster and easier way to create the GUI

Pandas: Pandas is used to analyze the data. It is made mainly for working with relational or labeled data

Pandas datareader: It allows to create a pandas Dataframe object by using various data sources

Numpy: Numpy is used for working with arrays and calculations

Matplotlib: Matplotlib is used to create 2D graphs and plots using python scripts

Datetime: Datetime module supplies classes for manipulating dates and times

Time: Provides various time-related functions

Beautifulsoup: Used for pulling data out of HTML and XML files

Requests: The requests module allows to send HTTP requests using Python

Copy: Used for copying the data and making changes to the copied data rather than original

Licensing: Library used for license key verification

Yfinance: It offers a threaded way to download market data from Yahoo finance


"""

############ WINDOW 1: AGREEMENT SCREEN #####################

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
from licensing.methods import Key, Helpers
import yfinance as yf
import fxcmpy

#Window 1 layout
win = tkinter.Tk()
win.geometry("770x500")
win.resizable (False, False)
win.iconbitmap('chart.ico') #location of the icon used
win.title (" Agreement Screen ")

#Opening next page
def next_page2():
   if result[0] == None or not Helpers.IsOnRightMachine(result[0]):
      ask = messagebox.askretrycancel(' Error', 'License Key incorrect...cannot submit!!!')
      if (ask == False):
         win.destroy()
      else:
         print()
   else:
      import windows2and3 #name other file windows2and3 and save it in the same folder

#Clear key function
def clearing():
   license_key_entry.delete(0,END)

#Not agreed
def not_agreed():
   messagebox.showerror(' Error', 'Cannot continue without agreement!!!')
   win.destroy()

#Title
title_label = Label(win, text = "Trading Analysis and Automated Trading", height = 3, font = "Arial 18 bold")
title_label.grid(row = 1, column = 1, sticky = W)

#Agreement options
agreement_label = Label(win, text = " Agree to proceed  ", height = 3, font = "Arial 13")
radio_button1 = Radiobutton (win, text = "I agree", value = "Agreed", font = "Arial 13", height = 1)
radio_button2 = Radiobutton (win, text = "I disagree", value = "Not agreed", command = not_agreed, font = "Arial 13", height = 1)
agreement_label.grid(column = 0, row = 4, sticky = W)
radio_button1.grid(column = 1, row = 4, sticky = W)
radio_button2.grid(column = 1, row = 5, sticky = W)

#License key authentication
RSAPubKey = "<RSAKeyValue><Modulus>sGbvxwdlDbqFXOMlVUnAF5ew0t0WpPW7rFpI5jHQOFkht/326dvh7t74RYeMpjy357NljouhpTLA3a6idnn4j6c3jmPWBkjZndGsPL4Bqm+fwE48nKpGPjkj4q/yzT4tHXBTyvaBjA8bVoCTnu+LiC4XEaLZRThGzIn5KQXKCigg6tQRy0GXE13XYFVz/x1mjFbT9/7dS8p85n8BuwlY5JvuBIQkKhuCNFfrUxBWyu87CFnXWjIupCD2VO/GbxaCvzrRjLZjAngLCMtZbYBALksqGPgTUN7ZM24XbPWyLtKPaXF2i4XRR9u6eTj5BfnLbKAU5PIVfjIS+vNYYogteQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyIyNTU1IiwiRjdZZTB4RmtuTVcrQlNqcSszbmFMMHB3aWFJTlBsWW1Mbm9raVFyRyJd=="
result = Key.activate(token=auth,\
                         rsa_pub_key=RSAPubKey,\
                         product_id=3349, \
                         key="abcd",\
                         machine_code=Helpers.GetMachineCode()) #add your key
   
def license_key():
   if result[0] == None or not Helpers.IsOnRightMachine(result[0]):
      # an error occurred or the key is invalid or it cannot be activated
      # (eg. the limit of activated devices was achieved)
      print("The license does not work: {0}".format(result[1]))
      messagebox.showerror(' Error', 'Incorrect License Key!!!')
   else:
      # everything went fine if we are here!
      print("The license is valid!")
      messagebox.showinfo('', 'License Key verified')
      license_key = result[0]
      print("Feature 1: " + str(license_key.f1))
      print("License expires: " + str(license_key.expires))
      
def remember_key():
   print("License key stored: ", license_key_store.get())
 
check_button = Checkbutton (win, text = "Remember", variable = "Remember", height = 2, command = remember_key, font = "Arial 12")
check_button.grid(column = 0, row = 12, sticky = W)

license_key_store = tkinter.StringVar()
license_key_label = Label (win, text = " License key:", height = 3, font = "Arial 12")
license_key_entry = Entry (win, width = 18, relief = GROOVE, textvariable = license_key_store)
license_button = Button (win, text = "< Verify >",command = license_key, font = "Arial 12", width = 8)
license_key_label.grid(column = 0, row = 8, sticky = W)
license_key_entry.grid(column = 1, row = 8, sticky = W, ipadx = 25, ipady = 3.7)
license_button.place(x = 315, y = 199)

#Submit button
submit_button = Button (win, text = "Submit", width = 12, command = next_page2, font = "Arial 12")
submit_button.place(x = 630, y = 450)

#Main loop
win.mainloop()
ip = input()
