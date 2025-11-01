

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS holdings;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS transfers;


CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    cash REAL DEFAULT 10000.00,  -- starting virtual balance
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- track user total holdings.
CREATE TABLE holdings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,          -- e.g. BTC, ETH
    name TEXT NOT NULL,            -- e.g. Bitcoin
    shares REAL NOT NULL,          -- amount of crypto held
    average_price REAL NOT NULL,   -- average price paid
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- track user transactions.
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares REAL NOT NULL,         
    price REAL NOT NULL,          
    total_value REAL NOT NULL,     
    type TEXT CHECK(type IN ('BUY', 'SELL')) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- allows users to make crypto transfer.

CREATE TABLE transfers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT DEFAULT 'completed',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
);


