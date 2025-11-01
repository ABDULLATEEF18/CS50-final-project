.

"# CS50-final-project"

PROJECT TITLE: crypto vault.

MY NAME: Atanda Abdullateef Ayodeji

GITHUB USERNAME: ABDULLATEEF18

EDX USERNAME: abdullateef_24

CITY AND COUNTRY: Lagos, Nigeria.

DATE RECORDED: 1/11/2025.

# YOUR PROJECT TITLE
Video Demo:  https://youtu.be/b04IIW3JQCI

Description: A flask web application built using flask framework, HTML, CSS, MYSQL(database), and jinja templates.
FEAUTURES:
auth: used normal logic and database verification to authenticate user.
buy crypto: used helper function to get live crypto prices, check the user balance and buy coin for the user.
sell crypto:  used helper function to get live crypto prices, check the user balance and sell coin for the user.
cash transfer: cash can be transfered from one user to another, would check if the user is eligible for the transfer and then transfer it.
portfolio: shows all the crypto holdings the user has.


# 💰 Crypto Vault

Crypto Vault is a Flask-based web application that allows users to **buy, sell, and track cryptocurrency holdings** securely.
It simulates a real-world crypto portfolio system — where users can log in, manage assets, and monitor their portfolio performance in real time.

---

## 🚀 Features

- 🧾 **User Authentication** — Secure login and session-based user management.
- 💸 **Buy & Sell Cryptos** — Record real-time transactions with price and quantity tracking.
- 📊 **Portfolio Dashboard** — View your total balance and crypto holdings.
- 💾 **Transaction History** — All buy/sell actions are logged in the `transactions` table.
- 🧮 **Dynamic Balance Calculation** — Portfolio value updates automatically based on transactions.
- ⚡ **Flask Blueprint Architecture** — Clean and modular app structure for scalability.

---
Project Structure

crypto_vault/
│
├── crypto_vault/
│ ├── init.py # App factory and configuration
│ ├── auth.py # User authentication routes
│ ├── routes.py # Main routes (dashboard, portfolio, etc.)
│ ├── helpers.py # Utility functions
│ ├── static/ # CSS, JS, and image assets
│ ├── templates/ # HTML templates
│ │ ├── layout.html
│ │ ├── login.html
│ │ ├── register.html
│ │ ├── index.html
│ │ ├── portfolio.html
│ │ ├── buy.html
│ │ ├── sell.html
│ └── database/
│ └── crypto_vault.sqlite
│
├── instance/ # Flask instance folder (ignored in git)
├── .venv/ # Virtual environment (ignored in git)
├── .gitignore
├── requirements.txt
└── run.py # Application entry point

🔮 Future Improvements

✅ Integrate real crypto market data from CoinGecko API

✅ Add email verification and 2FA

✅ Generate downloadable transaction reports

✅ Create a public API for external integrations

✅ Implement dark mode toggle



---

## 🧩 Database Schema

### 🧍‍♂️ Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| username | TEXT | Unique username |
| hash | TEXT | Hashed password |
| balance | REAL | User’s current account balance |

### 💱 Transactions Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key referencing users(id) |
| symbol | TEXT | Cryptocurrency symbol (e.g., BTC, ETH) |
| shares | REAL | Amount of crypto bought/sold |
| price | REAL | Price per unit |
| total_value | REAL | Total transaction value |
| type | TEXT | Either `BUY` or `SELL` |
| timestamp | TIMESTAMP | Time of transaction |

---

## 🌐 API Endpoints

### 🔹 **Authentication**
| Method | Endpoint | Description |
|---------|-----------|-------------|
| `GET` | `/register` | Show registration form |
| `POST` | `/register` | Register a new user |
| `GET` | `/login` | Show login form |
| `POST` | `/login` | Authenticate user and start session |
| `GET` | `/logout` | Log out current user and clear session |

---

### 🔹 **Homepage**
| Method | Endpoint | Description |
|---------|-----------|-------------|
| `GET` | `/` | Show homepage. If logged in, display user dashboard (username, balance). |

---

### 🔹 **Portfolio**
| Method | Endpoint | Description |
|---------|-----------|-------------|
| `GET` | `/portfolio` | Display user's owned cryptocurrencies, including symbol, total shares, total value, and current balance. |

---

### 🔹 **Buy Crypto**
| Method | Endpoint | Description |
|---------|-----------|-------------|
| `GET` | `/buy` | Render crypto purchase form |
| `POST` | `/buy` | Record a new **BUY** transaction, update user balance, and store in database |

---

### 🔹 **Sell Crypto**
| Method | Endpoint | Description |
|---------|-----------|-------------|
| `GET` | `/sell` | Render crypto sell form |
| `POST` | `/sell` | Record a **SELL** transaction, update holdings and balance accordingly |

---

### 🔹 **Transfer Cash**
| Method | Endpoint | Description |
|---------|-----------|-------------|
| `GET` | `/transfer` | Render transfer form |
| `POST` | `/transfer` | Transfer balance between users (optional feature) |

---

## ⚙️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/abdullateef18/crypto_vault.git
   cd crypto_vault





