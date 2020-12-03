import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for, abort, send_from_directory
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime

from helpers import *

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Upload configs
UPLOAD_FOLDER = "./static/uploads"
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024


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


@app.route("/")
@login_required
def index():

    # Get user id
    user_id = session["user_id"]

    # Template for users without bets
    if db.execute("SELECT COUNT(user) FROM userBets WHERE user = ?", user_id) == [{'COUNT(user)': 0}]:
        bets = [{'image': './static/uploads/bet-index-template.png'}]

    # Query for bets
    else:
        bets = db.execute("SELECT * FROM bets WHERE id IN (SELECT joined FROM userBets WHERE user = ?) "
                          "ORDER BY date LIMIT 3", user_id)

    return render_template("index.html", bets=bets)


@app.route("/newbet", methods=["GET", "POST"])
@login_required
def newbet():
    """Register new friendly bet"""
    if request.method == "POST":

        # Get user id
        user_id = session["user_id"]

        # Ensure title was submitted
        if not request.form.get("bname"):
            return apology("must provide a Title", 403)

        # Ensure entry requirement was submitted
        elif not request.form.get("entry"):
            return apology("must provide an entry requirement", 403)

        # Insert bet into db
        else:
            db.execute(
                "INSERT INTO bets (creator, title, requirements, date, address, about, format, image) "
                "VALUES (:creator, :title, :requirements, :date, :address, :about, :format, :image)",
                creator=user_id,
                title=request.form.get("bname"),
                requirements=request.form.get("entry"),
                date=request.form.get("date"),
                address=request.form.get("place"),
                about=None if request.form.get("about") == '' else request.form.get("about"),
                format=request.form.get("optradio"),
                image=upload_file())

            bet = db.execute("SELECT id FROM bets ORDER BY id DESC LIMIT 1")[0]["id"]

            # Creator joins bet
            db.execute(
                "INSERT INTO userBets (user, joined)"
                "VALUES (:user, :joined)",
                user=user_id,
                joined=bet)

            # Save bet invites sent
            invites = request.form.getlist("invited")
            if invites[0] == '':
                return redirect("/")

            else:
                for invite in invites:
                    db.execute("INSERT INTO userBets (user, invited) VALUES (:user, :invited)",
                               user=invite,
                               invited=bet)

                return redirect("/")

    else:
        return render_template("/newbet.html")


@app.route("/profile")
@login_required
def profile():
    """User's Profile"""
    return render_template("/profile.html")


@app.route("/mybets", methods=["GET", "POST"])
@login_required
def mybets():
    """User's ongoing bets"""
    user_id = session["user_id"]

    # View button route
    if request.method == 'POST':
        bet_id = request.form.get("bet")
        return redirect(url_for('bet_page', bet_id=bet_id))

    # Query for bets
    bets = db.execute("SELECT * FROM bets WHERE id IN (SELECT joined FROM userBets WHERE user = ?) "
                      "ORDER BY date", user_id)

    if not bets:
        return render_template("/mybets.html")

    else:
        return render_template("/mybets.html", bets=bets)


@app.route("/bet-page", methods=["GET", "POST"])
@login_required
def bet_page():
    """Bet info page"""
    user_id = session["user_id"]

    # Request arg with bet_id from url
    bet_id = request.args.get('bet_id', None)

    if request.method == 'POST':

        file = request.files['file']
        bet_img = db.execute("SELECT image FROM bets WHERE id=:bet_id", bet_id=bet_id)

        db.execute(
            "UPDATE bets"
            " SET "
            "title=:title,"
            "requirements=:requirements,"
            "date=:date,"
            "address=:address,"
            "about=:about,"
            "image=:image "
            "WHERE id=:bet_id",
            title=request.form.get("bname"),
            requirements=request.form.get("entry"),
            date=request.form.get("date"),
            address=request.form.get("place"),
            about=None if 'None' else request.form.get("about"),
            image=bet_img[0]['image'] if file.filename == '' else upload_file(),
            bet_id=bet_id)

        # Delete old img file
        new_bet_img = db.execute("SELECT image FROM bets WHERE id=:bet_id", bet_id=bet_id)
        if not new_bet_img == bet_img:
            delete_file(bet_img[0]['image'])

        return redirect(f"/bet-page?bet_id={bet_id}")

    else:

        # Query for bet info
        bet_info = db.execute("SELECT * FROM bets WHERE id = :bet_id", bet_id=bet_id)

        # Query for invites and joined info
        people = db.execute("SELECT * FROM userBets WHERE invited = :bet_id OR joined = :bet_id", bet_id=bet_id)

        return render_template("/bet-page.html/", bet=bet_info, user=user_id, people=people)


@app.route("/delete-bet")
@login_required
def delete_bet():

    # Get bet id from url
    bet_id = request.args.get('bet_id', None)

    # Get bet img url
    bet_img = db.execute("SELECT image FROM bets WHERE id=:bet_id", bet_id=bet_id)

    # Query to delete row from table
    db.execute("DELETE FROM bets WHERE id = :bet_id", bet_id=bet_id)
    delete_file(bet_img[0]['image'])

    return redirect("/mybets")


@app.route("/friends")
@login_required
def friends():
    """Show list of friends"""
    user_id = session["user_id"]

    list_of_friends = db.execute("SELECT user_two FROM friends WHERE user_one = :user_id", user_id=user_id)

    return render_template("friends.html", friends=list_of_friends)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorHandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorHandler)
