*Title: technical specification of algorithm trading back-test system
*Version: v0.1_20181203
*Author: Matthew Wang

## Introduction ##
This document layouts the technical details of the algorithm trading back-test system from data gathering and technical indicator construction to order execution and performance reporting. The process flow is formed by many modular functions which each is designed to perform a specific process. When applying a pre-defined algorithm, only one/two related modules need to be modified, others will remain the same for operational efficiency.

## Modules ##
1. Initial Setup: to define initial variables related to initial capital, trading vehicle, and risk management tools.
2. Data Preparation: to prepare the daily/intra-day price data to the desired trading frequency.
3. Indicator Creation: to create technical indicator(s) for use by the trading strategy
4. Order Identification: to identify long(buy) and short(sell) order by the pre-defined trading algorithm using technical indicators.
5. Trade Execution: to trade(long/short) based on the order instruction from the algorithm.
6. Performance Report: to construct performance and risk measures for trading strategy review.

## 1. Initial Setup ##
This module defines initial variables. 

* Testing time window (e.g. 02JAN2018 to 31OCT2018): defines the time period you want to test the algorithm performance.
	&start_date = 20180204; &end_date = 20181123;
* List of security tickers: contains a pool of tickers considered for trading, e.g. a list of fairly liquid stocks.
	&ticker_list = BAC AMD XLF F GM SIRI MU CMCSA…;
* Initial Capital: defines initial cash position, e.g. USD10,000
	&start_fund = 10000;
* Maximum number of stock holding: defines the max # of stock holding at any point of time to control over trading risk and transaction costs.
	&max_holding = 10;
* trade price buffer: defines the cost/lost due to transaction costs and possible delay in order execution.
	&trade_buffer = 0.01;
* market benchmark: defines the benchmark security used for algorithm performance comparison.
	&ticker_mkt = SPY;

## 2. Data Preparation ##
This module prepares time series data in the format applicable to the trade strategy and technical indicator creation.

The daily market data for a given security has table columns: TICKER, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME, CLOSE_ADJUSTED. For daily/weekly trade frequency algorithm, we will use the Closing price adjusted (CLOSE_ADJ) for split and dividend for simple technical indicator construction.

2.1) only include the in-scope tickers from the &ticker_list and populate their time series data of the CLOSE_ADJ for &start_date to &end_date.
2.2) for weekly trade frequency algorithm, convert the daily time series data to weekly data. The Friday/last trading date of the week data becomes the weekly data. 
e.g.  Daily time series data
Date	CLOSE_ADJ
2013-01-07 Mon	130.32
2013-01-08 Tue	129.94
2013-01-09 Wed	130.27
2013-01-10 Thu	131.31
2013-01-11 Fri	131.30*
to weekly data
Date/week	CLOSE_ADJ
  Sun, 6 Jan 2013	131.30*

## 3. Indicator Creation ##
This module creates technical indicator(s) for use of trading strategy.

For example of a simple trading strategy based on Simply Moving Average (SMA), for each TICKER two SMA need to be calculated: SMA_&slow and SMA_&fast where &slow and &fast are the pre-defined parameters indicating longer time period and shorter time period for SMA calculation. 

In this example we use &slow=16 and &fast=4 for TICKER=IBM. 
date	close_IBM	close_IBM_SMAslow16	close_IBM_SMAfast4
Sun, 6 Jan 2013	159.98	 	 
Sun, 13 Jan 2013	159.99	 	 
Sun, 20 Jan 2013	168.63	 	 
Sun, 27 Jan 2013	168.81	 	164.35
Sun, 3 Feb 2013	166.63	 	166.02
Sun, 10 Feb 2013	166.05	 	167.53
Sun, 17 Feb 2013	166.14	 	166.91
Sun, 24 Feb 2013	167.64	 	166.62
Sun, 3 Mar 2013	173.82	 	168.41
Sun, 10 Mar 2013	177.57	 	171.29
Sun, 17 Mar 2013	175.22	 	173.56
Sun, 24 Mar 2013	176.23	 	175.71
Sun, 31 Mar 2013	173.01	 	175.51
Sun, 7 Apr 2013	174.64	 	174.78
Sun, 14 Apr 2013	156.98	 	170.22
Sun, 21 Apr 2013	160.54	168.24	166.29
Sun, 28 Apr 2013	168.97	168.8	165.28
Sun, 5 May 2013	169.72	169.41	164.05

SMA_&slow = SMA_16 = average of PRICE_ADJ for the last 16 trading frequency. SMA_slow16 at the week of 21Apr2013 is the simple average of PRICE_ADJ for the past 16 weeks from the week of 6Jan2013 to 21Apr2013.

SMA_&fast = SMA_4 =  average of PRICE_ADJ for the last 4 trading frequency. SMA_slow4 at the week of 21Apr2013 is the simple average of PRICE_ADJ for the past 4 weeks from the week of 31Mar2013 to 21Apr2013.

## 4. Order Identification ##
This module identifies long(buy) and short(sell) order by the pre-defined trading algorithm.

For LONG/BUY orders, the idea is to compare the strength of the technical indicators among the pool of candidate TICKERS and pick the one with the strongest trend potential to invest.  
4.1) To construct a short-list of candidate TICKERS, only include TICKER with upward trend just established in the current date.
[GREEK] (SMA_fast/SMA_slow) in the current date > 1 and (SMA_fast/SMA_slow) in the previous date <=1
4.2) pick the TICKET with highest trend break magnitude
[GREEK] choose the TICKER with (SMA_fast/SMA_slow) = Max(SMA_fast/SMA_slow) for all candidate TICKERS
4.3) set the order type variable to 1 (LONG order) for the champion TICKER and 0 for other TICKERS.

For SHORT/SELL orders, short the TICKER once the downward trend breaks through.
4.4) to set the order type variable to -1 (SHORT odder) for the TICKER if downward trend breaks.
[GREEK] (SMA_fast/SMA_slow) in the current date < 1 and (SMA_fast/SMA_slow) in the previous date >=1

## 5. Trade Execution ##
This module carries out the trade execution according to the algorithm instruction. 

Before trading, a few house-keeping/risk management exercises need to be performed for the LONG/BUY order.
5.1) test whether capital is fully allocated, proceed only if the current holding count < the maximum number of TICKERS allowed.
[GREEK] count of current holding TICKERS < &max_holding
5.2) test whether the account already has the to-be-bought TICKER, proceed only if no current holding of the to-be-bought TICKER.
[GREEK] number of shares of the to-be-bought TICKER in the current holding = 0
5.3) long/buy the TICKER with order type = 1 (LONG/BUY). Order number of shares in integer (no fractional shares).
[GREEK] LONG number of shares = int[(&start_fund/&max_holding) / (CLOSE_ADJ*(1+&trade_buffer)]

For SHORT/SELL order, Sell all available shares in the holding.
5.4) test whether the account already has the to-be-sold TICKER, proceed only if there is current holding of the to-be-sold TICKER.
[GREEK] number of shares of the to-be-sold TICKER in the current holding > 0
5.5) short/sell the TICKER with order type = -1 (SHORT/SELL). 
[GREEK] SHORT all holding at the price = CLOSE_ADJ*(1-&trade_buffer)

After trading, need to keep track of a few accounting/risk measures
5.6) track accumulated # of trading transactions for cost/efficiency management
[GREEK] trade_count = accumulated trade_count in the previous date + the trade_count in the current date
5.7) track the number of TICKERs in the holding portfolio for portfolio size control
[GREEK] holding_count = count of TICKERS in the holding at the current date
5.8) track the cash position and portfolio validation for liquidity management.
[GREEK] cash (current cash position), mktvalue_TICKER = share_TICKER * price_TICKER

## 6. Performance Report ##
This module produces performance indicators for evaluate trading strategy performance.
For performance comparison, two benchmark algorithms are required. 
* All in SPY: LONG in SPY from day one and keep holding it.
* Equal weight: LONG in each of candidate TICKER for equal dollar size from day one and keep holding the portfolio.

A few performance is required for the champion trading strategy and the two benchmark strategies: 
6.1) Absolute return on investment (ROI): profitability on the initial investment
[GREEK] ROI at current date = sum(mktvalue_TICKER1, mktvalue_TICKER2, …) / &start_fund - 1
6.2) Annualized return rate (IRR): profitability of the initial investment on the annualized term
[GREEK] IRR at current date = [sum(mktvalue_TICKER1, mktvalue_TICKER2, …) / &start_fund] ** 1/(number of calendar days between portfolio start date and current date)/365 - 1
6.3) Sharpe ratio: evaluate the risk-adjusted return
[GREEK] Sharpe at current date = ?
6.4) Sortino ratio: evaluate the downside risk-adjusted return
[GREEK] Sortino at current date = ?
6.5) maximum drawdown: measures the decline from a historical peak in market value of the portfolio
[GREEK] max_drawdown = ?

## Analytical Module ##![image](https://github.com/iiiwater/Trading-Matthew/assets/35386869/a508e2c0-a062-41b9-9870-0c2674f3ef49)

Enhancement 2020
Principal: use algo to look for growth stock in upward trend (DMI, TRIX)
	1) Select stocks
		a. Screen new IPOs and drop outs
		b. Select stocks with adequate liquidity (price*volume>500k)
	2) Build indicators DMI, TRIX
	3) Run portfolio and common trigger + stop loss
	4) Tailor trigger based on analytic results
	5) Go live (weekly trading)
![image](https://github.com/iiiwater/Trading-Matthew/assets/35386869/f4005dbc-747d-46d1-9b43-218698ed8f50)
