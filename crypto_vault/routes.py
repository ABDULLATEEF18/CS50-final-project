from flask import Blueprint
import os
from .db import get_db
from .helpers import apology, login_required, lookup, usd
from random import randint


from flask import Flask, flash, redirect, render_template, request, session, url_for

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))






from flask import render_template

bp = Blueprint('routes', __name__)

@bp.route('/')
def hello():
    db = get_db()
    user_id = session.get("user_id")

    if user_id:
        user = db.execute(
            "SELECT username, cash FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
        return render_template("index.html", username=user["username"], balance=user["cash"])
    
    # Visitor mode — no user logged in
    return render_template("index.html", username=None, balance=None)


# route of buy, sell, and history
@bp.route("/buy", methods=["POST", "GET"])
@login_required
def buy_coin():  
    # two inputs, coin to buy and amount.
     # Get current user ID
    if request.method == "POST":
        coin = request.form.get("coin")
        if not coin:
            return apology("input coin to buy!", 400)
        amount = request.form.get("amount")
        if not amount:
            return apology("input an amount to buy!", 400)
        amount = int(amount)
        coin = coin.lower()
        lookups = lookup(coin, currency="usd")
        # validate lookup
        if not lookups:
            return apology("server failed so bad", 400)
        price = lookups["price"]
        price = int(price)
         # check the total price
        total_cost = price * amount
        db = get_db()
        #get the user_id
        user_id = session["user_id"]
        row = db.execute("SElECT * FROM users WHERE id=?", (user_id,)).fetchall()
        #check user cash
        user_cash = row[0]["cash"]
        if user_cash > total_cost:
            # update cash
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (total_cost, user_id))
            # insert into transactions
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, total_value, type) VALUES(?,?,?,?,?,?)",
                      (user_id, coin.upper(),amount, price,total_cost, "BUY"))
            db.commit()
            flash("successful purchase")
            return redirect("/")
            
        else:
            return apology("not enough cash!", 400)     
            
    else:
        return render_template("buy.html")
# write the sell route.
@bp.route("/sell", methods=["POST", "GET"])
@login_required
def sell_coin(): 
# check the request method
       if request.method == "GET":
           # render sell template
           db = get_db()
           user_id = session["user_id"]
           row = db.execute("SELECT cash FROM users WHERE id = ?", (user_id,)).fetchone()
           user_cash = row["cash"] if row else 0
           return render_template("sell.html", user_cash=user_cash)     
       else:
           user_id = session["user_id"]
           symbol = request.form.get("symbol")
           if not symbol:
               return apology("input coin to buy!", 400)
           shares = request.form.get("shares")
           if not shares:
               return apology("input coin to buy!", 400)
           shares = int(shares)
           if shares <= 0:
            return apology("shares must be a positive integer", 400)

           # query database
           db = get_db()
           row = db.execute("SELECT sum(shares) as total_shares FROM transactions WHERE symbol=? AND user_id=?", (symbol, user_id)).fetchone()
           owned = row["total_shares"] if row and row["total_shares"] is not None else 0
           owned = int(owned)
           # validate if what he owns is more than what he wants to sell
           if (owned < shares):
               # means he is eligible to sell
               # get price of the coin
               stock = lookup(symbol, currency="usd")
               if not stock:
                    return apology("sorry, our api failed", 400)
               current_price = stock["price"]
               current_price= int(current_price)
               #check total price
               total_price = current_price * shares
               # update transactions
               db.execute("INSERT INTO transactions (user_id, symbol, shares, price, total_value, type) VALUES(?,?,?,?,?,?)",
                      (user_id, symbol.upper(), shares, current_price,total_price, "SELL"))
               # update cash balance
               db.execute("UPDATE users SET cash= cash + ? WHERE id=?", (total_price, user_id))
               db.commit()
           else:
               return apology("sorry, not enough shares!", 400)
           flash("sale of coin is a success!")
           
           return redirect("/")
           
# create endpoint for crypto transfer

@bp.route("/transfer", methods=["GET", "POST"])
@login_required
def cash_transfer():
    db = get_db()
    user_id = session["user_id"]

    # GET: Show transfer page with current balance
    if request.method == "GET":
        row = db.execute("SELECT cash FROM users WHERE id = ?", (user_id,)).fetchone()
        cash = row["cash"] if row else 0
        return render_template("transfer.html", user_cash=cash)

    # POST: Handle transfer
    username = request.form.get("username")
    cashh = request.form.get("cash")

    # --- Input validation ---
    if not username or not cashh:
        return apology("Please provide both username and amount.", 400)

    try:
        cashh = float(cashh)
        if cashh <= 0:
            return apology("Amount must be greater than zero.", 400)
    except ValueError:
        return apology("Invalid amount entered.", 400)

    # --- Get sender's balance ---
    row = db.execute("SELECT cash FROM users WHERE id = ?", (user_id,)).fetchone()
    if not row:
        return apology("User not found.", 400)
    sender_cash = float(row["cash"])

    # --- Validate balance ---
    if cashh > sender_cash:
        return apology("Insufficient balance.", 400)

    # --- Validate receiver ---
    receiver = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    if not receiver:
        return apology("Receiver username does not exist.", 400)

    receiver_id = receiver["id"]

    # --- Prevent self-transfer ---
    if receiver_id == user_id:
        return apology("You cannot transfer to yourself.", 400)

    # --- Perform the transfer atomically ---
    try:
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (cashh, user_id))
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", (cashh, receiver_id))
        db.commit()
    except Exception as e:
        db.rollback()
        print("Transfer Error:", e)
        return apology("Transaction failed. Please try again.", 500)

    flash(f"Transfer of ${cashh:.2f} to {username} successful!")
    return redirect("/")

# now lets build our homepage.

@bp.route("/homepage")
#@login_required
def homepage():
    """Homepage route for CryptoVault"""

    # If user not logged in, show landing page
    if not session.get("user_id"):
        return render_template("homepage.html")

    # If user logged in, fetch data from database
    db = get_db()
    user = db.execute(
        "SELECT username, balance FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    # Handle invalid sessions (user not found)
    if user is None:
        session.clear()
        return redirect(url_for("auth.login"))

    # Render homepage with user info
    return render_template(
        "index.html",
        username=user["username"],
        balance=user["balance"]
    )
 



@bp.route("/portfolio")
@login_required
def portfolio():
    db = get_db()
    user_id = session["user_id"]

    # Aggregate total holdings per crypto symbol
    rows = db.execute("""
        SELECT symbol,
               SUM(CASE WHEN type = 'BUY' THEN shares ELSE -shares END) AS total_shares,
               AVG(price) AS avg_price
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, (user_id,)).fetchall()

    # Calculate total portfolio value from stored prices
    portfolio = []
    total_value = 0

    for row in rows:
        current_value = row["total_shares"] * row["avg_price"]
        total_value += current_value
        portfolio.append({
            "symbol": row["symbol"],
            "shares": row["total_shares"],
            "price": row["avg_price"],
            "value": current_value
        })

    return render_template("portfolio.html", portfolio=portfolio, total_value=total_value)