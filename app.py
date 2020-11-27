import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import *

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///betaum.db")

"""
# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
"""


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide E-mail", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid E-mail and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached reached route via POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password meet requirements
        elif len(request.form.get("password")) < 6:
            return apology("Password needs to be bigger or equal to six characters", 403)

        # Ensure password and confirmation match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("Passwords don't match", 403)

        # Ensure username is unique
        elif db.execute("SELECT * FROM users WHERE email = :email",
                        email=request.form.get("email")):
            return apology("E-mail used in another account", 403)

        # Insert user in database with hashed password
        else:
            db.execute("INSERT INTO users (email, firstname, lastname, hash) VALUES (:email, :firstname, :lastname, "
                       ":hash)",
                       email=request.form.get("email"),
                       firstname=request.form.get("firstname"),
                       lastname=request.form.get("lastname"),
                       hash=generate_password_hash(request.form.get("password")))
            return redirect("/")

    # User reached reached route via GET
    if request.method == "GET":
        return render_template("/register.html")


@app.route("/newbet", methods=["GET", "POST"])
@login_required
def newbet():
    """Register new friendly bet"""
    return render_template("/newbet.html")


@app.route("/profile")
@login_required
def profile():
    """User's Profile"""
    return render_template("/profile.html")


@app.route("/mybets")
@login_required
def mybets():
    """User's ongoing bets"""
    return render_template("/mybets.html")


@app.route("/friends")
@login_required
def friends():
    """User's friends"""
    return render_template("/friends.html")




def errorHandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorHandler)
