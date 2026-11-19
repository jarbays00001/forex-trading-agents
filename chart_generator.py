import yfinance as yf
import mplfinance as mpf
import pandas as pd
import sys
import datetime
import os

# Menerima argumen dari terminal (ticker, entry, sl, tp, signal)
ticker = sys.argv[1]
entry = float(sys.argv[2])
sl = float(sys.argv[3])
tp = float(sys.argv[4])
signal = sys.argv[5]

# Ambil data 30 hari terakhir
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=30)

print(f"Mengunduh data untuk {ticker}...")
df = yf.download(ticker, start=start_date, end=end_date, interval="1d", progress=False)

if df.empty:
    print("Data kosong, gagal membuat chart.")
    sys.exit(1)

# yfinance sering menggunakan MultiIndex, kita rapikan jika perlu
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df.index = df.index.tz_localize(None)

# Konfigurasi garis horizontal (Entry, SL, TP)
# Warna: Biru (Entry), Merah (SL), Hijau (TP)
hlines = dict(hlines=[entry, sl, tp], colors=['#2196F3', '#F44336', '#4CAF50'], linestyle='--', linewidths=1.5)

# Konfigurasi warna candlestick (Hijau naik, Merah turun)
mc = mpf.make_marketcolors(up='#4CAF50', down='#F44336', edge='inherit', wick='inherit', volume='in')
s  = mpf.make_mpf_style(marketcolors=mc, gridstyle=':', y_on_right=True, facecolor='#1E1E1E', edgecolor='#1E1E1E', figcolor='#1E1E1E', rc={'axes.labelcolor': 'white', 'xtick.color': 'white', 'ytick.color': 'white', 'text.color': 'white'})

# Simpan chart
chart_file = 'trade_chart.png'
title = f'{ticker} - {signal} Setup'

mpf.plot(df, type='candle', style=s, title=title, hlines=hlines, savefig=chart_file, figratio=(12,8), volume=False, tight_layout=True)
print(f"Chart berhasil disimpan ke {chart_file}")
