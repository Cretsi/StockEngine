# app.py - v1.1

from flask import Flask, render_template, request
import yfinance as yf
import plotly.graph_objs as go
from plotly.offline import plot

from indicators import compute_ichimoku, compute_rsi, compute_macd, compute_bollinger_bands

app = Flask(__name__)

indicator_descriptions = {
    "ichimoku": 
'''Ichimoku Cloud:
The Ichimoku Cloud, also known as Ichimoku Kinko Hyo, is a versatile indicator that provides information on trend direction, support, and resistance levels, and potential buy or sell signals.
The Ichimoku Cloud consists of five lines:

- Tenkan-sen (Conversion Line): The midpoint of the highest high and the lowest low over the past nine periods.
- Kijun-sen (Base Line): The midpoint of the highest high and the lowest low over the past 26 periods.
- Senkou Span A (Leading Span A): The average of the Tenkan-sen and Kijun-sen, projected 26 periods ahead.
- Senkou Span B (Leading Span B): The midpoint of the highest high and the lowest low over the past 52 periods, projected 26 periods ahead.
- Chikou Span (Lagging Span): The current closing price, plotted 26 periods behind.
  The space between Senkou Span A and Senkou Span B forms the Ichimoku Cloud.

To interpret the Ichimoku Cloud:

The cloud provides support and resistance levels. If the stock price is above the cloud, it indicates a bullish trend. If the price is below the cloud, it indicates a bearish trend.
A thick cloud signifies strong support or resistance, while a thin cloud indicates weak support or resistance.
If Senkou Span A is above Senkou Span B, the cloud is green and indicates bullish sentiment. If Senkou Span A is below Senkou Span B, the cloud is red and indicates bearish sentiment.
To utilize the Ichimoku Cloud:

Look for potential buy signals when the stock price crosses above the cloud and the cloud is green. The Tenkan-sen and Kijun-sen should also cross above the cloud for confirmation.
Look for potential sell signals when the stock price crosses below the cloud and the cloud is red. The Tenkan-sen and Kijun-sen should also cross below the cloud for confirmation.
Use the Ichimoku Cloud in conjunction with other technical indicators to confirm buy or sell signals and avoid false breakouts.

''',
    "rsi": "The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements. It ranges from 0 to 100 and is typically used to identify overbought or oversold conditions in a market.",
    "macd": "The Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security's price.",
    "bollinger_bands": "Bollinger Bands are a type of statistical chart characterizing the prices and volatility over time of a financial instrument, using a formulaic method and standard deviations."
}


@app.route("/", methods=["GET", "POST"])
def index():
    graphs = {}
    if request.method == "POST":
        stock_ticker = request.form["stock_ticker"]
        selected_indicators = request.form.getlist("indicators")

        data = get_stock_data(stock_ticker)
        graphs = create_stock_indicator_graphs(data, selected_indicators)

        return render_template("graphs.html", graphs=graphs, descriptions=indicator_descriptions, stock_ticker=stock_ticker)

    return render_template("index.html")

def get_stock_data(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period="1y")
        return stock_data
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

def create_stock_indicator_graphs(stock_data, selected_indicators):
    indicator_functions = {
        "ichimoku": compute_ichimoku,
        "rsi": compute_rsi,
        "macd": compute_macd,
        "bollinger_bands": compute_bollinger_bands
    }

    graphs = {}
    for key, func in indicator_functions.items():
        if key in selected_indicators:
            graph = func(stock_data)
            graphs[key] = plot(graph, output_type="div", include_plotlyjs=True)

    return graphs

if __name__ == "__main__":
    app.run(debug=True)
