from flask import render_template, redirect, url_for, flash
from market import app, db
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/market")
@login_required
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user_to_create = User(username=register_form.username.data,
                              email_address=register_form.email_address.data,
                              password=register_form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account Created Successfully! You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))
    
    if register_form.errors != {}:
        for error in register_form.errors.values():
            flash(f"There was an error while creating an user: {error}", category="danger")

    return render_template("register.html", register_form=register_form)


@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        attempted_user = User.query.filter_by(username=login_form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=login_form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and Password not match! Please try again', category='danger')
            
    return render_template("login.html", login_form = login_form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('home_page'))
    




