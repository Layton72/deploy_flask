from recipes_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from recipes_app.models.users import Users
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/login')
def login():
    if "logged_in" in session:
        return redirect('/recipes')
    if "errors" in session and session["errors"] == True:
        email = session.pop("email", None)
        session["errors"] = False
        return render_template("login.html", email=email)
    return render_template('login.html')

@app.route('/login/process', methods=['POST'])
def process_login():
    if not Users.validate_login(request.form):
        session["errors"] = True
        session["email"] = request.form["email"]
        return redirect('/login')
    else:
        session["logged_in"] = Users.get_one_by_email(request.form["email"]).id
        return redirect('/recipes')

@app.route('/register')
def render_register():
    if "logged_in" in session:
        return redirect('/recipes')
    if "errors" in session and session["errors"] == True:
        first_name = session.pop("first", None)
        last_name = session.pop("last", None)
        birthday = session.pop("birthday", None)
        email = session.pop("email", None)
        session["errors"] = False
        return render_template('register.html', first_name=first_name, last_name=last_name, birthday=birthday, email=email)
    return render_template('register.html')

@app.route('/register/process', methods=["POST"])
def process_register():
    if not Users.validate_user(request.form):
        session["errors"] = True
        session["first"] = request.form["first_name"]
        session["last"] = request.form["last_name"]
        session["birthday"] = request.form["birthday"]
        session["email"] = request.form["email"]
        return redirect("/register")
    else:
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "birthday": request.form["birthday"],
            "email": request.form["email"],
            "password": bcrypt.generate_password_hash(request.form['password'])
        }
        Users.save(data)
        session["logged_in"] = Users.get_one_by_email(request.form["email"]).id
        return redirect('/recipes')


@app.route('/welcome')
def welcome():
    if "logged_in" not in session:
        return redirect ('/login')
    
    name = Users.get_one_by_id(session["logged_in"]).first_name
    return render_template('welcome.html', name=name)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
