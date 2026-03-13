import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from arch import arch_model
from scipy.optimize import minimize

# --- PHẦN 1: GARCH VOLATILITY FORECASTING ---
def run_volatility_engine(ticker="HPG.VN"):
    df = yf.download(ticker, start="2024-01-01", end="2026-03-13")
    df['Returns'] = 100 * np.log(df['Close'] / df['Close'].shift(1))
    df = df.dropna()

    model = arch_model(df['Returns'], vol='Garch', p=1, q=1)
    res = model.fit(disp='off')
    
    # Dự báo 5 ngày
    forecast = res.forecast(horizon=5)
    print(f"\nForecasted Volatility for {ticker}:", np.sqrt(forecast.variance.values[-1, :]))
    
    # Vẽ biểu đồ Volatility
    plt.figure(figsize=(10, 5))
    plt.plot(res.conditional_volatility, color='teal', label='GARCH Volatility')
    plt.title(f'Volatility Analysis: {ticker}')
    plt.legend()
    plt.savefig('volatility_report.png')
    plt.show()

# --- PHẦN 2: EFFICIENT FRONTIER (SIMULATION) ---
def plot_efficient_frontier():
    # Giả lập 3 tài sản: HPG, VCB, VIC (Hoặc các mã VN30)
    tickers = ['HPG.VN', 'VCB.VN', 'VIC.VN']
    data = yf.download(tickers, start="2024-01-01")['Close']
    returns = data.pct_change().dropna()
    
    num_portfolios = 2000
    results = np.zeros((3, num_portfolios))
    
    for i in range(num_portfolios):
        weights = np.random.random(3)
        weights /= np.sum(weights)
        
        p_ret = np.sum(returns.mean() * weights) * 252
        p_vol = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
        
        results[0,i] = p_ret
        results[1,i] = p_vol
        results[2,i] = p_ret / p_vol # Sharpe Ratio

    plt.figure(figsize=(10, 6))
    plt.scatter(results[1,:], results[0,:], c=results[2,:], cmap='viridis', marker='o', s=10, alpha=0.3)
    plt.colorbar(label='Sharpe Ratio')
    plt.title('Efficient Frontier: VN30 Selection')
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.savefig('efficient_frontier.png')
    plt.show()

if __name__ == "__main__":
    run_volatility_engine()
    plot_efficient_frontier()