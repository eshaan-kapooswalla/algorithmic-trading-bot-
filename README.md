# 🚧 Algorithmic Trading Bot (Under Development) 🚧

> **Note:** This project is currently under active development. Features, structure, and documentation are subject to change as the bot evolves.

---

## 📈 Algorithmic Trading Bot

Welcome to the Algorithmic Trading Bot project! This repository contains the foundational code and structure for building a robust, automated trading system using the Binance Testnet. The bot is designed for research, backtesting, and live (paper) trading, with a focus on modularity, security, and professional software practices.

---

## 🌟 Features
- **Secure API Key Management**: Credentials are loaded from a `.env` file and never committed to version control.
- **Robust Binance API Client**: Encapsulated in `core_logic/client.py` with resilient error handling and retry logic.
- **Historical Data Fetching**: Retrieve candlestick (k-line) data for any symbol and interval.
- **Real-Time Price Fetching**: Get the latest price for any trading pair instantly.
- **Account Info**: Fetch and display balances for key assets.
- **Professional Project Structure**: Clean separation of concerns for scalability and maintainability.

---

## 🗂️ Project Structure
```
algorithmic-trading-bot/
├── .env.example           # Example environment variables (never commit your real .env!)
├── .gitignore             # Ensures secrets and virtual environments are not tracked
├── README.md              # Project documentation (you're reading it!)
├── requirements.txt       # All Python dependencies (exact versions)
├── config/                # Configuration files (future expansion)
├── core_logic/            # Main trading logic and Binance API client
│   └── client.py          # Encapsulated, resilient Binance API client
├── data/                  # Data storage (historical, logs, etc.)
├── src/                   # Entry points and orchestration scripts
├── utils/                 # Utility functions and helpers
└── venv/                  # Python virtual environment (not tracked)
```

---

## 🚀 Getting Started

1. **Clone the repository**
   ```sh
   git clone https://github.com/eshaan-kapooswalla/algorithmic-trading-bot-.git
   cd algorithmic-trading-bot
   ```
2. **Set up a Python virtual environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure your environment variables**
   - Copy `.env.example` to `.env` and fill in your Binance Testnet API keys.
   - Never commit your real `.env` file!
5. **Run the client test**
   ```sh
   python core_logic/client.py
   ```

## Data Processing & Technical Indicators

- The `utils/helpers.py` module now includes:
  - `klines_to_dataframe`: Converts raw Binance kline data (list of lists) to a pandas DataFrame with proper columns and types.
  - `add_indicators`: Adds common technical indicators (SMA, EMA, RSI) to a DataFrame using the `pandas-ta` library.
- Ensure you have `pandas-ta` installed (see requirements.txt).

---

## 🛡️ Security & Best Practices
- **Never** commit your `.env` file or real API keys.
- All sensitive files are protected by `.gitignore`.
- The bot uses the Binance Testnet for safe, risk-free development and testing.

---

## 📚 Further Reading & Resources
- [python-binance Documentation](https://python-binance.readthedocs.io/en/latest/)
- [Binance Testnet](https://testnet.binance.vision/)
- [Twelve-Factor App: Config](https://12factor.net/config)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 📝 License
MIT License 