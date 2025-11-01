
import os
from flask import Blueprint

from flask import Flask, flash, redirect, render_template, request, session
#from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash 

from .db import get_db

from .helpers import apology, login_required, lookup, usd

# implement login, logout and register.   
bp = Blueprint('auth', __name__)


# implement logout
#@bp.route('/logout', methods=['GET', 'POST'])
db = get_db

@bp.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # login a user
    
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        #verify username
        if not username:
             return apology("username must be provided", 400)
        password = request.form.get("password")
        #verify password
        if not password:
             return apology("username must be provided", 400)
         # query the database for username.
        db = get_db()
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)).fetchall()
         # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"],  password ):
             return apology("invalid username and/or password", 403)
        # who loged in? always do this at every login attempt.
        session["user_id"] = rows[0]["id"]
        
        user = db.execute(
        "SELECT username, cash FROM users WHERE id = ?",
        (session["user_id"],)
         ).fetchone()


        return redirect("/")
        #return render_template("index.html",  username=user["username"],balance=user["cash"])
    else:
        return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
#@login_required    made a serious mistake here.
def register():
    """Register user"""
    if request.method == "POST":
        # verify username and password
        username = request.form.get("username")
        if not username:
             return apology("username must be provided", 400)
         
        password_1 = request.form.get("password")
        if not password_1:
             return apology("password must be provided", 400)
         
        hashed_password= generate_password_hash(password_1)
        
        password_2 = request.form.get("confirmation")
        if not password_2:
            return apology("you must confirm password", 400)
        # initialize the database
        db = get_db()
           
        # verify passwords
        if password_1 == password_2:
            rows = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
            
            if len(rows) > 0:
                return apology("user already exist", 400)
            
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (username,hashed_password))
            # close database
            db.commit()
            
            flash("Registration successful! You can now log in.")
            return redirect("/login")
        else:
                return apology("password not confirmed.")
    else:
        return render_template("register.html")
    