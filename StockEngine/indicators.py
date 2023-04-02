# indicators.py - v1.1

import pandas as pd
import numpy as np
import ta
import plotly.graph_objs as go
import pandas_ta as pta
from finta import TA

import numpy as np

def compute_ichimoku(data: pd.DataFrame) -> go.Figure:
    high_prices = data['High']
    low_prices = data['Low']
    close_prices = data['Close']
    
    tenkan_sen = (high_prices.rolling(9).max() + low_prices.rolling(9).min()) / 2
    kijun_sen = (high_prices.rolling(26).max() + low_prices.rolling(26).min()) / 2
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
    senkou_span_b = ((high_prices.rolling(52).max() + low_prices.rolling(52).min()) / 2).shift(26)
    chikou_span = close_prices.shift(-26)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=tenkan_sen, name="Tenkan-sen"))
    fig.add_trace(go.Scatter(x=data.index, y=kijun_sen, name="Kijun-sen"))

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=senkou_span_a,
            name="Senkou Span A",
            fill=None,
            mode="lines",
            line_color="rgba(255, 102, 102, 0.5)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=senkou_span_b,
            name="Senkou Span B",
            fill="tonexty",
            mode="lines",
            line_color="rgba(255, 102, 102, 0.5)",
        )
    )

    fig.add_trace(go.Scatter(x=data.index, y=chikou_span, name="Chikou Span"))

    fig.update_layout(title="Ichimoku Cloud", yaxis_title="Price")
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(180, 180, 180, 0.5)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(180, 180, 180, 0.5)")

    return fig




def compute_rsi(stock_data: pd.DataFrame, period: int = 14):
    close_prices = stock_data['Close']
    delta = close_prices.diff().dropna()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    data = [go.Scatter(x=stock_data.index, y=rsi, mode='lines', name='RSI')]

    layout = go.Layout(title='Relative Strength Index (RSI)', xaxis=dict(title='Date'), yaxis=dict(title='RSI'))

    return {"data": data, "layout": layout}

def compute_macd(stock_data: pd.DataFrame, short_period: int = 12, long_period: int = 26, signal_period: int = 9):
    close_prices = stock_data['Close']
    exp12 = close_prices.ewm(span=short_period, adjust=False).mean()
    exp26 = close_prices.ewm(span=long_period, adjust=False).mean()

    macd_line = exp12 - exp26
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()

    data = [
        go.Scatter(x=stock_data.index, y=macd_line, mode='lines', name='MACD Line'),
        go.Scatter(x=stock_data.index, y=signal_line, mode='lines', name='Signal Line'),
        go.Bar(x=stock_data.index, y=(macd_line - signal_line), name='Histogram')
    ]

    layout = go.Layout(title='Moving Average Convergence Divergence (MACD)', xaxis=dict(title='Date'), yaxis=dict(title='MACD'))

    return {"data": data, "layout": layout}

def compute_bollinger_bands(stock_data: pd.DataFrame, window: int = 20, num_std: int = 2):
    close_prices = stock_data['Close']
    rolling_mean = close_prices.rolling(window=window).mean()
    rolling_std = close_prices.rolling(window=window).std()

    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)

    data = [
        go.Scatter(x=stock_data.index, y=upper_band, mode='lines', name='Upper Band'),
        go.Scatter(x=stock_data.index, y=lower_band, mode='lines', name='Lower Band', fill='tonexty'),
        go.Scatter(x=stock_data.index, y=rolling_mean, mode='lines', name='Rolling Mean'),
        go.Scatter(x=stock_data.index, y=stock_data['Close'].values, mode='lines', name='Close'),

    ]

    layout = go.Layout(title='Bollinger Bands', xaxis=dict(title='Date'), yaxis=dict(title='Price'))

    return {"data": data, "layout": layout}
