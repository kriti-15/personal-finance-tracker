# ============================================================
# STOCK PRICE ANALYZER
# Fetches real stock data and analyzes trends using Python
# Libraries used: yfinance (data), pandas (analysis),
#                 matplotlib (charts)
# ============================================================

# Install required libraries by running:
#   pip install yfinance pandas matplotlib

import yfinance as yf       # Downloads real stock/index data from Yahoo Finance
import pandas as pd         # Data analysis library (like Excel for Python)
import matplotlib.pyplot as plt  # Creates charts and graphs
from datetime import datetime, timedelta


# ──────────────────────────────────────────────
# STEP 1: Download stock data
# ──────────────────────────────────────────────

def get_stock_data(ticker, days=90):
    """
    Downloads historical stock price data.

    Parameters:
        ticker : Stock symbol, e.g. 'RELIANCE.NS' (NSE India), 'AAPL' (Apple USA)
        days   : How many past days of data to fetch (default: 90)

    Returns:
        A pandas DataFrame with columns: Open, High, Low, Close, Volume
    """
    end_date   = datetime.today()
    start_date = end_date - timedelta(days=days)

    print(f"\n📡 Fetching data for: {ticker} (last {days} days)...")

    # yf.download fetches data from Yahoo Finance — no API key needed!
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True, progress=False)

    if data.empty:
        print("❌ No data found. Check the ticker symbol.")
        return None

    print(f"✅ Downloaded {len(data)} rows of data.")
    return data


# ──────────────────────────────────────────────
# STEP 2: Compute simple statistics
# ──────────────────────────────────────────────

def analyze_stock(data, ticker):
    """
    Calculates basic statistics about a stock:
    - Highest and lowest closing price
    - Average closing price
    - Total return (% gain/loss over the period)
    - 7-day and 30-day moving averages
    """
    close = data["Close"]  # We focus on the daily closing price

    highest  = close.max()
    lowest   = close.min()
    average  = close.mean()
    start    = close.iloc[0]   # First day's price
    end      = close.iloc[-1]  # Last day's price
    returns  = ((end - start) / start) * 100  # Percentage change

    # Moving averages smooth out daily noise to show trends
    data["MA7"]  = close.rolling(window=7).mean()   # 7-day moving average
    data["MA30"] = close.rolling(window=30).mean()  # 30-day moving average

    print(f"\n📊 Analysis for {ticker}")
    print("─" * 40)
    print(f"  📈 Highest Close  : ₹/$ {float(highest):,.2f}")
    print(f"  📉 Lowest  Close  : ₹/$ {float(lowest):,.2f}")
    print(f"  📐 Average Close  : ₹/$ {float(average):,.2f}")
    print(f"  🔄 Period Return  : {float(returns):+.2f}%")

    if returns > 0:
        print("  ✅ Stock is UP over this period.")
    elif returns < 0:
        print("  ⚠️  Stock is DOWN over this period.")
    else:
        print("  ➡️  Stock is flat over this period.")

    return data


# ──────────────────────────────────────────────
# STEP 3: Plot the chart
# ──────────────────────────────────────────────

def plot_stock(data, ticker):
    """
    Creates a line chart showing:
    - Daily closing price
    - 7-day moving average
    - 30-day moving average

    The chart is saved as a PNG file.
    """
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={"height_ratios": [3, 1]})

    # --- Top chart: Price + moving averages ---
    ax1 = axes[0]
    ax1.plot(data.index, data["Close"], label="Closing Price", color="#2196F3", linewidth=1.5)
    ax1.plot(data.index, data["MA7"],   label="7-Day MA",      color="#FF9800", linewidth=1.2, linestyle="--")
    ax1.plot(data.index, data["MA30"],  label="30-Day MA",     color="#4CAF50", linewidth=1.2, linestyle="--")

    ax1.set_title(f"{ticker} — Stock Price Analysis", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Price")
    ax1.legend()
    ax1.grid(alpha=0.3)

    # --- Bottom chart: Volume (how many shares traded each day) ---
    ax2 = axes[1]
    ax2.bar(data.index, data["Volume"].squeeze(), color="#9C27B0", alpha=0.6, width=0.8)
    ax2.set_ylabel("Volume")
    ax2.set_xlabel("Date")
    ax2.grid(alpha=0.3)

    plt.tight_layout()

    filename = f"{ticker.replace('.', '_')}_analysis.png"
    plt.savefig(filename, dpi=150)
    print(f"\n✅ Chart saved as '{filename}'")
    plt.show()


# ──────────────────────────────────────────────
# STEP 4: Compare two stocks
# ──────────────────────────────────────────────

def compare_stocks(ticker1, ticker2, days=90):
    """
    Compares the normalized performance of two stocks.
    Normalizing means both start at 100 so we can fairly compare growth %.

    Example: compare_stocks("RELIANCE.NS", "TCS.NS")
    """
    data1 = get_stock_data(ticker1, days)
    data2 = get_stock_data(ticker2, days)

    if data1 is None or data2 is None:
        return

    # Normalize: start both at 100 for a fair comparison
    norm1 = (data1["Close"] / data1["Close"].iloc[0]) * 100
    norm2 = (data2["Close"] / data2["Close"].iloc[0]) * 100

    plt.figure(figsize=(12, 5))
    plt.plot(norm1.index, norm1, label=ticker1, color="#2196F3", linewidth=2)
    plt.plot(norm2.index, norm2, label=ticker2, color="#F44336", linewidth=2)

    plt.axhline(100, color="gray", linewidth=0.8, linestyle="--")  # Starting baseline
    plt.title(f"Performance Comparison: {ticker1} vs {ticker2}", fontsize=13, fontweight="bold")
    plt.ylabel("Normalized Price (Base = 100)")
    plt.xlabel("Date")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    filename = f"comparison_{ticker1.split('.')[0]}_vs_{ticker2.split('.')[0]}.png"
    plt.savefig(filename, dpi=150)
    print(f"✅ Comparison chart saved as '{filename}'")
    plt.show()


# ──────────────────────────────────────────────
# MAIN MENU
# ──────────────────────────────────────────────

def main():
    print("╔═══════════════════════════════╗")
    print("║   📈 Stock Price Analyzer      ║")
    print("╚═══════════════════════════════╝")
    print("\nTicker examples:")
    print("  Indian stocks : RELIANCE.NS  TCS.NS  INFY.NS  HDFCBANK.NS")
    print("  US stocks     : AAPL  MSFT  GOOGL  AMZN  TSLA")

    while True:
        print("\n1. Analyze a stock")
        print("2. Compare two stocks")
        print("3. Quit")
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            ticker = input("Enter ticker symbol: ").strip().upper()
            days   = int(input("Days of history (e.g. 90): ").strip())
            data   = get_stock_data(ticker, days)
            if data is not None:
                data = analyze_stock(data, ticker)
                plot_stock(data, ticker)

        elif choice == "2":
            t1 = input("First ticker : ").strip().upper()
            t2 = input("Second ticker: ").strip().upper()
            days = int(input("Days of history (e.g. 90): ").strip())
            compare_stocks(t1, t2, days)

        elif choice == "3":
            print("👋 Goodbye!")
            break


if __name__ == "__main__":
    main()
