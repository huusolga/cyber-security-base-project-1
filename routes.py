from flask import redirect, render_template, abort, request, session
"""
Flaw 2: Cryptographic Failures


from werkzeug.security import check_password_hash
"""

from secrets import token_hex
from app import app
import sql

def check_user():
    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            return abort(403)
    except KeyError:
        return abort(403)
    
def clear_errors():
    session["passwords_differ"] = False
    session["username_in_use"] = False
    session["registration_successful"] = False

@app.route("/")
def index():
    clear_errors()
    try:
        todos = sql.get_todos(session["username"])
    except KeyError:
        todos = []
    return render_template("index.html", count=len(todos), todos=todos)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_again = request.form["password_again"]
        if password != password_again:
            session["passwords_differ"] = True
            return redirect("/register")
        if sql.add_user(username, password):
            clear_errors()
            session["registration_successful"] = True
            return redirect("/")
        elif not sql.add_user(username, password):
            session["username_in_use"] = True
            return redirect("/register")

@app.route("/login", methods=["POST"])
def login():
    """
    Fix 5: Security Logging and Monitoring failures

    Code below limits the amount of logins

    if session["attempts"] >= 30:
        return redirect(request.referrer)
    """
    username = request.form["username"]
    password = request.form["password"]
    user = sql.get_user(username)
    if not user:
        session["invalid_user"] = True
        return redirect(request.referrer)
    else:
        """
        Fix 2: Cryptographic failures

        Code below uses function check_password_hash which checks whether the hashed correct password
        and the hashed password from user input match. 

        hash = user.password
        if check_password_hash(hash, password):
        """
        if password == user.password:
            session["user_id"] = user.id
            session["username"] = username
            session["admin"] = user.admin
            session["invalid_user"] = False
            """
            Fix 5: Security Logging and Monitoring Failures

            session["attempts"] = 0
            """
            session["csrf_token"] = token_hex(16)
        else:
            session["invalid_user"] = True
            """
            Fix 5: Security Logging and Monitoring Failures

            session["attempts"] += 1
            """
            return redirect(request.referrer)
    return redirect(request.referrer)

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    del session["admin"]
    del session["invalid_user"]
    del session["csrf_token"]
    return redirect("/")

@app.route("/admin_page")
def admin():
    """ 
    Fix 1: Broken Access Control

    try:
        if not session['admin']:
            return redirect("/")
    except KeyError:
        return redirect("/")
    """
    clear_errors()
    users = sql.get_users()
    return render_template("admin.html", users=users)

@app.route("/create", methods=["POST"])
def create():
    check_user()
    content = request.form["content"]
    if session["username"]:
        sql.create_todo(content, session["username"])
    return redirect("/")

@app.route("/delete_todo/<int:id>", methods=["POST"])
def delete_todo(id):
    sql.remove_todo(id)
    return redirect("/")
    

@app.route("/delete_user/<int:id>", methods=["POST"])
def delete_user(id):
    check_user()
    sql.remove_user(id)
    return redirect(request.referrer)
