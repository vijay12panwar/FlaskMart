from flask import render_template, redirect, url_for, flash
from market import app, db
from market.models import Item, User
from market.forms import RegisterForm

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/market")
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user_to_create = User(username=register_form.username.data,
                              email_address=register_form.email_address.data,
                              password_hash=register_form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    
    if register_form.errors != {}:
        for error in register_form.errors.values():
            flash(f"There was an error while creating an user: {error}", category="danger")

    return render_template("register.html", register_form=register_form)
