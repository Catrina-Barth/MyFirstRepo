"""
This program generates a simple website called Check-In by using python flask.
"""

# Imported modules
import time

import flask
from flask import Flask, request, render_template
from passlib.hash import sha256_crypt

#A folder where the users form can be uploaded
UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

LOGGEDIN = False


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    """
    The app.route that holds the uploaded data from the users form
    """
    if not LOGGEDIN:
        return render_template("login_temp.html", msg="")

    if request.method == 'POST':
        firstname = flask.request.form["firstname"]
        lastname = flask.request.form["lastname"]
        city = flask.request.form["city"]
        state = flask.request.form["state"]
        status = flask.request.form["status"]
        date = flask.request.form["date"]
        photo = flask.request.form["photo"]

        f_d = open("users/" + lastname + firstname + ".txt", "a")
        f_d.write(firstname + "\n")
        f_d.write(lastname + "\n")
        f_d.write(city + "\n")
        f_d.write(state + "\n")
        f_d.write(status + "\n")
        f_d.write(date + "\n")
        f_d.write(photo + "\n")
        f_d.close()
        return render_template("home.html")
    else:
        return render_template('check_in.html')



@app.route('/')
@app.route('/home')
def hello():
    """
    The app.route to the html home page
    """
    now = time.ctime()
    print(now)
    return render_template("home.html", now = now)


# The app.route to the html about us page
@app.route('/about_us')
def about_us():
    """
    About us page python directions
    """
    return render_template("about_us.html")



@app.route('/register', methods=['GET', 'POST'])
def login():
    """
    The app.route to the html login screen where user enters Username and Password
    """
    if flask.request.method == "POST":
        username = flask.request.form["username"]
        password = flask.request.form["password"]
        error = None
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
            flask.flash(error)

        if len(password) < 12 or not any(letter.islower() for letter in password) or \
                not any(letter.isupper() for letter in password) or \
                not any(letter.isdigit() for letter in password) or \
                not any(letter in "@$#:%&!*$" for letter in password):
            return render_template("register.html", msg="""Password should include at least
            12 characters in length, and
            include at least 1 uppercase character, 
            1 lowercase character, 1 number and 1 special character""")
        if error is None:
            f_d = open("secret.txt", "a")

            f_d.write(username + "|")

            f_d.write(sha256_crypt.hash(password) + "\n")
        return render_template("home.html", username=username)
    else:
        return render_template("register.html")



@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """
    The app.route to the html login screen where user enters Username and Password
    """
    global LOGGEDIN
    if flask.request.method == "POST":
        username = flask.request.form["username"]
        password = flask.request.form["password"]
        error = None
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
            flask.flash(error)


        if error is None:
            f_d = open("secret.txt", "r")
            for line in f_d:
                line = line.strip()
                info = line.split("|")
                try:
                    if info[0] == username and sha256_crypt.verify(password, info[1]):
                        LOGGEDIN = True
                except:
                    LOGGEDIN = False

            if not LOGGEDIN:
                return render_template("login_temp.html", msg="Incorrect user name and/or password")

            return render_template("home.html", username=username)
    else:
        return render_template("login_temp.html", msg="")





@app.route("/download_search", methods=['GET'])
def download_search():
    """
    The app.route to the html search page
    """
    if not LOGGEDIN:
        return render_template("login_temp.html", msg="")
    return render_template('/download_search')

@app.route("/search", methods=['GET', 'POST'])
def search():
    """
    The function that has directions for the search html page
    """
    if not LOGGEDIN:
        return render_template("login_temp.html", msg="")
    if flask.request.method == "POST":
        firstname = flask.request.form["firstname"]
        lastname = flask.request.form["lastname"]
        try:
            f_d = open("users/" + lastname + firstname + ".txt", "r")
        except:
            return render_template("/search_result.html", person="notfound")
        person = dict()
        person["firstname"] = f_d.readline()
        person["lastname"] = f_d.readline()
        person["city"] = f_d.readline()
        person["state"] = f_d.readline()
        person["status"] = f_d.readline()
        person["date"] = f_d.readline()
        person["photo"] = f_d.readline()
        f_d.close()
        return render_template("/search_result.html", person=person)

    else:
        return render_template('/search.html')
