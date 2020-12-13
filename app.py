import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for, abort, send_from_directory
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import date

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


@app.route("/")
@login_required
def index():
    # Get user id
    user_id = session["user_id"]
    today = str(date.today())

    bets = db.execute("SELECT * FROM bets WHERE id IN (SELECT joined FROM userBets WHERE user = ?) "
                      "ORDER BY date LIMIT 3", user_id)
    bets.insert(0, {'date': today, 'image': './static/uploads/bet-index-template.png'})

    return render_template("index.html", bets=bets, today=today)


# /------------------------------------------ USER RELATED ROUTES ----------------------------------------------------/


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
        session["user_id"] = rows[0]["user"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """User's Profile"""
    user_id = session["user_id"]
    profile_id = request.args.get('id', None)

    if request.method == "POST":

        # Add user to friend list
        addressed_user = profile_id
        if not user_id == addressed_user:

            db.execute("INSERT INTO friends (request_user, addressed_user) VALUES (:request_user, :addressed_user)",
                       request_user=user_id, addressed_user=addressed_user)

    else:
        profile_info = db.execute("SELECT firstname, lastname, avatar FROM users "
                                  "WHERE user = :profile_id", profile_id=profile_id)

        friended_users = get_friends(profile_id)[0]

        friend_button = get_friends(user_id)[0]
        friend_id_list = [d['user'] for d in friend_button]

        friend_check = 1 if int(profile_id) in friend_id_list else 0

    return render_template("/profile.html/",
                           profile_info=profile_info, profile_id=profile_id,
                           user_id=str(user_id), friended_users=friended_users,
                           friend_check=friend_check)


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """User's Profile"""
    user_id = session["user_id"]

    user_info = db.execute("SELECT firstname, lastname, avatar FROM users WHERE user = :user_id", user_id=user_id)

    return render_template("/settings.html", user_info=user_info)


@app.route("/upload-profile-picture", methods=["POST"])
@login_required
def upload_profile_picture():
    user_id = session["user_id"]

    user_avatar = db.execute("SELECT avatar FROM users WHERE user = :user_id", user_id=user_id)

    delete_old_avatar(user_avatar[0]['avatar'])
    filepath = upload_avatar(user_id)

    my_file = filepath
    base = os.path.splitext(my_file)[0]
    os.rename(my_file, base + '.png')

    filepath = f'static/uploads/avatars/{user_id}.png'

    db.execute("UPDATE users SET avatar = :avatar WHERE user = :user_id", user_id=user_id, avatar=filepath)

    return redirect(f"/profile?id={user_id}")


@app.route("/change-password", methods=["POST"])
@login_required
def newPassword():
    """Manage Account Settings"""
    user_id = session["user_id"]

    # Query database for username
    rows = db.execute("SELECT * FROM users WHERE email = :email",
                      email=request.form.get("email"))

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("old-password")):
        return apology("invalid username and/or password", 403)

    if not request.form.get("password"):
        return apology("must provide password", 403)

    # Ensure password meet requirements
    if len(request.form.get("password")) < 6:
        return apology("Password needs to be bigger or equal to six characters", 403)

    # Ensure password and confirmation match
    elif request.form.get("confirmation") != request.form.get("password"):
        return apology("Passwords don't match", 403)

    db.execute("UPDATE users SET hash = :hash WHERE user = :user_id",
               hash=generate_password_hash(request.form.get("password")), user_id=user_id)

    return redirect("/")


@app.route("/add-friend")
@login_required
def add_friend():
    """Invite profile owner as friend"""
    user_id = session["user_id"]
    profile_id = request.args.get('id', None)

    # Check if a invite was sent
    former_invite = db.execute("SELECT addressed_user "
                               "FROM friends "
                               "WHERE request_user = :user_id AND addressed_user = :profile_id",
                               user_id=user_id, profile_id=profile_id)

    if not len(former_invite) == 0:
        return redirect(f"/profile?id={profile_id}")

    db.execute("INSERT INTO friends (request_user, addressed_user) VALUES (:request_user, :addressed_user)",
               request_user=user_id, addressed_user=profile_id)

    return redirect(f"/profile?id={profile_id}")


@app.route("/friends")
@login_required
def friends():
    """Show list of friends"""
    user_id = session["user_id"]

    func_return = get_friends(user_id)

    friended_users = func_return[0]
    friend_requests = func_return[1]

    return render_template("friends.html", requests=friend_requests, friends=friended_users)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# /-------------------------------------------- BET RELATED ROUTES ----------------------------------------------------/


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

        else:

            # Insert bet into db
            db.execute(
                "INSERT INTO bets (creator, title, requirements, date, address, about, format, image) "
                "VALUES (:creator, :title, :requirements, :date, :address, :about, :format, :image)",
                creator=user_id,
                title=request.form.get("bname"),
                requirements=request.form.get("entry"),
                date=date.today() if request.form.get("date") == '' else request.form.get("date"),
                address="Online" if request.form.get("place") == "" else request.form.get("place"),
                about=None if request.form.get("about") == "" else request.form.get("about"),
                format=request.form.get("optradio"),
                image=upload_file())

            # Get biggest(equals latest) bet id
            bet = db.execute("SELECT id FROM bets ORDER BY id DESC LIMIT 1")[0]["id"]

            # Creator joins bet
            db.execute(
                "INSERT INTO userBets (user, joined)"
                "VALUES (:user, :joined)",
                user=user_id,
                joined=bet)

            # Save bet invites sent
            invites = request.form.getlist("invited")

            # Remove any duplicates in invites
            invites = list(dict.fromkeys(invites))

            if len(invites) == 0 or invites[0] == "Choose friend...":
                return redirect("/")

            else:
                for invite in invites:
                    db.execute("INSERT INTO userBets (user, invited) VALUES (:user, :invited)",
                               user=invite,
                               invited=bet)

                return redirect("/")

    else:
        user_id = session["user_id"]

        func_return = get_friends(user_id)

        friended_users = func_return[0]

        return render_template("/newbet.html", friends=friended_users)


@app.route("/my-bets", methods=["GET", "POST"])
@login_required
def my_bets():
    """User's ongoing bets"""
    user_id = session["user_id"]

    # View button route
    if request.method == 'POST':
        bet_id = request.form.get("bet")
        return redirect(url_for('bet_page', bet_id=bet_id))

    # Query for joined bets
    bets = db.execute("SELECT * FROM bets WHERE id IN (SELECT joined FROM userBets WHERE user = ?) "
                      "ORDER BY date", user_id)

    # Query for invited bets
    inv_bets = db.execute("SELECT * FROM bets WHERE id IN (SELECT invited FROM userBets WHERE user = ?) "
                          "ORDER BY date DESC", user_id)

    if not bets:
        return render_template("/my-bets.html")

    else:
        today = str(date.today())
        return render_template("/my-bets.html", bets=bets, inv_bets=inv_bets, today=today)


@app.route("/bet-page", methods=["GET", "POST"])
@login_required
def bet_page():
    """Bet info page"""
    user_id = session["user_id"]

    # Request arg with bet_id from url
    bet_id = request.args.get('bet_id', None)

    if request.method == 'POST':

        # Get img from form
        file = request.files['file']

        # Get bet img url from db
        bet_img = db.execute("SELECT image FROM bets WHERE id=:bet_id", bet_id=bet_id)

        # Update db table
        db.execute(
            "UPDATE bets"
            " SET "
            "title = :title,"
            "requirements = :requirements,"
            "date = :date,"
            "address = :address,"
            "about = :about,"
            "image = :image "
            "WHERE id = :bet_id",
            title=request.form.get("bname"),
            requirements=request.form.get("entry"),
            date=request.form.get("date"),
            address=request.form.get("place"),
            about=None if '' else request.form.get("about"),
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
        people = db.execute(
            "SELECT * FROM userBets "
            "INNER JOIN users USING(user) "
            "WHERE invited = :bet_id OR joined = :bet_id", bet_id=bet_id)

        friended_users = get_friends(user_id)[0]

        return render_template("/bet-page.html/", bet=bet_info, user=user_id, people=people, friends=friended_users)


@app.route("/invite-friend", methods=["GET", "POST"])
@login_required
def invite_friend():
    """Invites a friend to join bet"""
    if request.method == 'POST':

        # Request arg with bet_id from url
        bet_id = request.args.get('bet_id', None)

        # Save bet invites sent
        invited = request.form.getlist("invited")

        # Remove any duplicates in invited
        invites = list(dict.fromkeys(invited))
        invites = [int(i) for i in invites]

        # Query for users that joined or were invited previously
        on_bet = db.execute("SELECT user FROM userBets WHERE joined = :bet_id OR invited = :bet_id", bet_id=bet_id)
        not_invite = [d['user'] for d in on_bet]

        for invite in not_invite:
            if invite in invites:
                invites.remove(invite)

        if len(invites) == 0 or invites[0] == "Choose friend...":
            return redirect(f"/bet-page?bet_id={bet_id}")

        else:
            for invite in invites:
                db.execute("INSERT INTO userBets (user, invited) VALUES (:user, :invited)",
                           user=invite,
                           invited=bet_id)

            return redirect(f"/bet-page?bet_id={bet_id}")


@app.route("/delete-bet")
@login_required
def delete_bet():
    """Delete a bet"""

    # Get bet id from url
    bet_id = request.args.get('bet_id', None)

    # Get bet img url
    bet_img = db.execute("SELECT image FROM bets WHERE id = :bet_id", bet_id=bet_id)

    # Query to delete row from table
    db.execute("DELETE FROM bets WHERE id = :bet_id", bet_id=bet_id)
    delete_file(bet_img[0]['image'])

    return redirect("/my-bets")


@app.route("/join-bet")
@login_required
def join_bet():
    """User join a bet"""
    user_id = session["user_id"]

    # Get bet id from url
    bet_id = request.args.get('bet_id', None)

    # Update db table
    db.execute(
        "UPDATE userBets"
        " SET "
        "invited = :invited, "
        "joined = :joined "
        "WHERE invited = :bet_id AND user = :user_id",
        invited=None,
        joined=bet_id,
        bet_id=bet_id,
        user_id=user_id)

    return redirect("/my-bets")

# /--------------------------------------------------------------------------------------------------------------------/

# Error handlers

def errorHandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


for code in default_exceptions:
    app.errorhandler(code)(errorHandler)
