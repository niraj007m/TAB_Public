## Model overview
The model is an automated trading model offering the trading functionalities altogether in a single frame which otherwise is distributed on different websites or spaces. Analysis of trading as well can be done. 
<br>
It provides parameters like checking the latest ask price of any ticker, using indicators like SMA, EMA, MACD, RSI, etc. to visualize the ticker price over a particular time interval. Trading the number of slots asked by the user, analysis of the ticker using strategies and getting to know the topmost active tickers presently, are some more features of the system.
<br><br>

## Concepts/components:
### Basic concepts
•	Share/stock market- Platform where buyers and sellers meet to exchange equity shares<br>
•	OHLCV- Open High Low Close Volume is an aggregated form of market data<br>
•	Backtesting in stock market- Method of checking how well a specific market strategy would have done<br>
•	KPI- Key Performance Indicator is a quantifiable measure of performance over time for a specific objective<br>
•	API- Application Programming Interface is the bridge between two applications which lets them communicate with each other<br>
•	Ticker- It reports transaction and price data for a security, updated continuously throughout the day<br>
•	Technical indicators- Fundamental part of technical analysis and typically plotted as a chart pattern to try to predict the market trend

### Indicators
•	Moving average: Smooths the price data to form a trend following indicator<br>
•	Simple Moving Average (SMA): Formed by computing the average price of a security over a specific number of periods<br>
•	Exponential Moving Average (EMA): Reduces the lag by applying more weight to recent prices<br>
•	Moving Average Convergence/Divergence (MACD): Turns two trend-following indicators/moving averages, into a momentum oscillator<br>
•	Bollinger Bands (BB): Volatility bands placed above and below a moving average<br>
•	Relative Strength Index (RSI): Momentum oscillator that measures the speed and change of price movements<br>
•	Average True Range (ATR): Indicator that measures volatility<br>
•	Average Directional Index (ADX): Derived from the smoothed averages of the difference between +DI and -DI. Measures strength of the trend over time<br>

### Libraries used
•	Tkinter: Tkinter is the standard GUI library used. Python when combined with Tkinter provided a faster and easier way to create the GUI<br>
•	Pandas: Pandas is used to analyze the data. It is made mainly for working with relational or labeled data<br>
•	Pandas datareader: It allowed to create a pandas Dataframe object by using various data sources<br>
•	Numpy: Numpy is used for working with arrays and calculations<br>
•	Matplotlib: Matplotlib is used to create 2D graphs and plots using python scripts<br>
•	Datetime: Datetime module supplies classes for manipulating dates and times<br>
•	Time: Provides various time-related functions<br>
•	Beautifulsoup: Used for pulling data out of HTML and XML files<br>
•	Requests: The requests module allows to send HTTP requests using Python<br>
•	Copy: Used for copying the data and making changes to the copied data rather than original<br>
•	Licensing: Library used for license key verification<br>
•	Yfinance: It offers a threaded way to download market data from Yahoo finance<br>
•	Fxcmpy: It provides a wrapper class for the API provided by FXCM<br>

## GUI
Window 1 is the agreement screen. It comprises of the agreement option and the license key verification which is to be taken as input from the user. 
The user can also store the license key.<br><br>
![win1](https://user-images.githubusercontent.com/79084332/190449390-bc62d6e1-78a2-4c4e-af3b-a8abc8037e42.jpg)<br><br>
Window 2 is the trading screen. It offers the functionalities of checking the ask price of any particular ticker, using indicators (SMA, EMA, MACD, RSI, etc.) to visualize the ticker data, 
trading the number of slots user provides as input, checking the analysis of the ticker using backtracking on the window 3 and checking the top 10 active tickers.<br><br>
![win2](https://user-images.githubusercontent.com/79084332/190449902-944d4b22-382c-47b1-9fa9-e11f5b45ec33.jpg)<br><br>
Checking for ticker value and verifying it on Yahoo Finance website.<br><br>
![win2 ticker entered](https://user-images.githubusercontent.com/79084332/190449926-8bc24d51-81d5-4ea1-98f2-8abb2c58d7d1.jpg)<br><br>
![yf ticker entered](https://user-images.githubusercontent.com/79084332/190449996-d359c764-6e20-44dd-bab9-943ed7244e11.jpg)<br><br>
Using the MACD indicator for visualizing the ticker data<br><br>
![MACD for ticker](https://user-images.githubusercontent.com/79084332/190450100-cdeb7d4a-ccae-49ee-8d0e-87a5dfe83440.jpg)<br><br>
Display top 10 active tickers<br><br>
![top 10](https://user-images.githubusercontent.com/79084332/190451144-025d822f-6d73-465d-adf9-c8a366622e96.jpg)<br><br>
Window 3 displays the graph of the ticker which uses backtracking using buy and hold strategy compared to portfolio rebalancing strategy.<br><br>
![win3](https://user-images.githubusercontent.com/79084332/190450735-17a1e046-d461-48b4-90f7-fc7f9ceb94a0.jpg)<br><br>
![graph of ticker](https://user-images.githubusercontent.com/79084332/190451190-ffcb9928-4732-4e08-94fe-cd0e594ccaf6.jpg)<br><br>
