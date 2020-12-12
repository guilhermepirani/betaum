import os
from cs50 import SQL
import requests
import urllib.parse

from flask import redirect, render_template, session, request
from functools import wraps

from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
UPLOAD_FOLDER = "./static/uploads"

db = SQL("sqlite:///betaum.db")


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename,):

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "./static/uploads/bet-img-template.png"
        file = request.files['file']

        # submit a empty part without filename
        if file.filename == '':
            return "./static/uploads/bet-img-template.png"

        # Save file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            return "./static/uploads/{}".format(filename)


def delete_file(old_file):
    template = "./static/uploads/bet-img-template.png"
    if os.path.exists(old_file):
        if not old_file == template:
            os.remove(old_file)


def upload_avatar(user_id):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "./static/img/user.svg"
        file = request.files['file']

        # submit a empty part without filename
        if file.filename == '':
            return "./static/img/user.svg"

        # Save file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_extension = os.path.splitext(filename)
            file.save(os.path.join('static/uploads/avatars', str(user_id) + file_extension[1]))

            return f"./static/uploads/avatars/{user_id}{file_extension[1]}"


def delete_old_avatar(old_file):
    template = "./static/img/user.svg"
    if os.path.exists(old_file):
        if not old_file == template:
            os.remove(old_file)


def get_friends(user_id):
    """Show list of friends"""

    inc_friend = db.execute(
        "SELECT * FROM users WHERE user IN ("
        "SELECT request_user FROM friends WHERE addressed_user = :user_id) ORDER BY firstname", user_id=user_id)

    out_friend = db.execute(
        "SELECT * FROM users WHERE user IN ("
        "SELECT addressed_user FROM friends WHERE request_user = :user_id) ORDER BY firstname", user_id=user_id)

    friend_requests = []
    friended_users = []

    for friend in inc_friend:
        if friend in out_friend:
            friended_users.append(friend)
        else:
            friend_requests.append(friend)

    return [friended_users, friend_requests]
