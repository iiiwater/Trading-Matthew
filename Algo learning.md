Type of traders
· Day traders: intraday, use simple technical analysis including support/resistance and patterns
· Swing traders: 1day to 1 month, use technical analysis including oscillators
· Position traders: 1 month to 1 year, use technical analysis and fundamental analysis
	 
Summary of technical indicator types
· Short-term indicators based on closing prices
	o MACD, RSI, PPO, PMO, TSI, TRIX, Pring's KST, etc.
· Short-term indicators based on OHLC prices
	o Fast/Slow Stochastics, Full Stochastics, % William R, Aroon, DMI/ADX, Parabolic SAR, Vortex Indicator, RVI, CCI, Ultimate Oscillator, etc.
· Money flow indicators
	o Money flow index, Chaikin money flow, OBV, VMAP, Force index, Ease of Movement, etc.
· Longer-term indicators
	o Pring's Special K, Coppock Curve, etc.
· Trading bands and overlays
	o Moving average envelope, Bollinger bands, Keltner Channel, Donchian Channel, Tim Fong's Band, Chandelier Exit, Ichimoku Clouds, etc.
 
PPO
· Is a MACD based on percentage change 
	o so standardized and comparable.
· Formula
	o PPO = 100*[EMA12d(Close) - EMA26d(Close)]/EMA26d(Close)
	o Signal line = EMA9d(PPO)
	o PPO histogram = PPO-Signal line
· Trading: buy when PPO>Signal, Sell when PPO<Signal
 
TRIX
· It measures percentage change of a triple exponentially smoothed moving average
	o Smoother than MACD with less whipsaws
	o Tends to turn a bit later
· Formula
	o Triple-smoothed EMA= EMA15d{EMA15d[EMA15d(Close)]}
	o TRIX=100*[triple EMA -triple EMA(-1d)]/triple EMA(-1d)
	o Single line = EMA9d(TRIX)
·  Trading: buy if TRIX>Signal line
 
Stochastic
· It is an oscillator using Close, High, Low prices. The idea is that the closing prices should predominantly close in the same direction as the prevailing trend.
· Formula: Full Stochastic(n,i,j), default (14,3,3), better (14,5,5)
	o Full %K=SMA_i(100 × (Close −MIN_n(Low))/(MAX_n(High)−MIN_n(Low) ))
	o Full %D=SMA_j(Full %K)
DMI
· It is used to figure out trending condition in the decision tree
 
Chandelier Exit
· It sets a trailing stop-loss based on the average true range.
· Formula:
	o CE_uptrend(n,i)=MAX_n(High)−i ×ATR(n)
	o CE_downtrend(n,i)=MIN_n(Low)+i ×ATR(n)
	o ATR(n)=MAX
 
DMI/ADX
· a
 
Elder's Impulse System
· It combines two powerful indicators: EMA_13d (market trend) and MACD (momentum)
· Formula
	o Green price bar: EMA(Close,13) > EMA-1d(Close,13) and MACD histogram > MACD histogram-1d
	o Red price bar: EMA(Close,13) < EMA-1d(Close,13) and MACD histogram < MACD histogram-1d
	o Blue price bar: not Green or Red conditions
	 
Decision tree
 
Decision flow	 	 	 	 
	 		Not trending	 
 Is it trending?		 Trending
		        · space		        · space
 When did the cross happen?	 + space		 + space
Indicator:	TRIX	TRIX	Full Stochastic	Full Stochastic
		Weak		Weak
 Slope of the indicator when it crossed?	 Strong		 Strong
Action:	Trade	Wait	Trade	Wait
 
Machine Learning to add value in 
· Tree learning
· Neural network (tensorflow)
· Support vector machine
 
 
Indicator	Use	Logic	Rule
Market Level	 	 	 
Market trend	Overall rule to permit action	SPY's MA (65d) > MA (195d)	 
Stock screening	 	 	 
EPS growth	A degree of EPS growth, and > peers	 	 
Revenue growth	Sales growth, and > peers	 	 
ROE	High ROE => management effectively uses resources	 	 
Insider transactions	Asymmetric information	 	 
Float	Available shares on the open market	 	 
Short float	Lower short interest	 	 
Debt to equity ratio	Lower DE v.s. peers	 	 
Fair value	To identify bargain price	Quarterly earning * 4 * avg PE	Allow 10% discount for trading point (4 wks), 20% for 20 wks
Stock Level	 	 	 
Moving Average	Find trend reversing point, filter the purchase and shorting entry action.	fast MA > slow MA, uptrend. Fast MV < slow MV, downtrend	40d and 120d MA
Donchian Channels	highest and lowest price over a set period of time, e.g. 50 days	 	40d Donchian Channel
	Ensure the uptrend still attracts new buyers. Buy stocks which are making new highs, sell those making new lows.
Volume	institutional conviction in the new highs	volume > volume moving average * multiple	20d MA of volume * 1.5
Stochastics oscillator	signal when price has a statistically significant move against the overall trend, give a low risk entry.	%D (20,3,1), reading < 10 => oversold, >90 => overbought	%D (20,3,1)
Average true range indicator (ATR)	Average range in $ during a given period	4.5*ATR(14d)	 
	Indication of volatility	Or use 4.5*ATR/price to create % (caveats to trailing stop-losses)
	[Stop-loss] To set stop-losses and position size
	 
Bollinger Band	A band plotted two stdev away from a SMA	20 days SMA	Long if price<lower & upward trend
	Measure of volatility	Upper and lower bands (2 stdev)	Short if price>upper & downward trend
	Increase volatile -> increase band
	Price closes to upper band: overbought
	[Entry]&[Exit] To set entry point for long and short
Action	 	 	 
Purchase	 	Enter on the open of a day that follows the signal	 
![image](https://github.com/iiiwater/Trading-Matthew/assets/35386869/be80384e-931c-4fe9-904c-6bbc6b6593f9)

  SMA & EMA
https://www.investopedia.com/terms/e/ema.asp
Function syntax: SMA(var,d)  where var: variable name, d: number of days/periods
Function syntax: EMA(var,d)  where var: variable name, d: number of days/periods

TRIX
· It measures percentage change of a triple exponentially smoothed moving average
	o Smoother than MACD with less whipsaws
	o Tends to turn a bit later
	o https://www.tradingview.com/scripts/trix/
· Formula
	o Triple-smoothed EMA= EMA15d{EMA15d[EMA15d(Close)]}
	o TRIX=100*[triple EMA -triple EMA(-1d)]/triple EMA(-1d)
Function syntax: TRIX(var,d)  where var: variable name, d: number of days/periods
 
Stochastic
· It is an oscillator using Close, High, Low prices. The idea is that the closing prices should predominantly close in the same direction as the prevailing trend.
https://en.wikipedia.org/wiki/Stochastic_oscillator
· Formula: Full Stochastic(n,i,j), default (14,3,3), better (14,5,5)
	o Full %K=SMA_i(100 × (Close −MIN_n(Low))/(MAX_n(High)−MIN_n(Low) ))
	o Full %D=SMA_j(Full %K)
Function syntax: TRIX(var,d)  where var: variable name, d: number of days/periods

![image](https://github.com/iiiwater/Trading-Matthew/assets/35386869/e230f2bb-02d9-451f-9eb2-9e339c6f16f3)
