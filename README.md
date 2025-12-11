# TraderBot 🦾

A simple, extensible trading bot for **Bybit**, built with Python and `pybit`.

Supports RSI and MACD strategies that you can enable dynamically at startup.

---

## 🚀 Features

- 📈 Technical indicators: **RSI** and **MACD**
- ⚙️ Environment-based configuration (`.env` or shell variables)
- 💱 Automatic Take-Profit and Stop-Loss management
- 🧩 Strategy selection at startup (`--strategy rsi`, `--strategy macd`, or both)
- 🧠 Clean, modular codebase (exchange / strategies / bot loop)
- ✅ Works with **Bybit Unified Trading API**

---

## 🧰 Requirements

- Python **3.10+**
- A Bybit API key (for Testnet or Live)
- `pip` installed

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/xperemiquel/traderbot.git
cd traderbot
```

Create and activate a virtual environment:

````bash
python -m venv .venv
source .venv/bin/activate   # on Linux/macOS
# or
.\.venv\Scripts\activate    # on Windows
````

Install dependencies:

```bash
pip install -r requirements.txt
```

IDEAS:
conectar CHATGPT para leer las principales noticias y investir en base a eso (enfocar en un mercado)
Operar en base a la tasa de interes de estados unidos (cuando sube suben las cryptos)




