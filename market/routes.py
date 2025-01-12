from flask import render_template, redirect, url_for, flash, request
from market import app, db
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/market", methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        purchased_item = request.form.get('purchase_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(item_price=p_item_object.price):
                p_item_object.assign_ownership(user=current_user)
                flash(f'Congratulations! You have successfully purchased {purchased_item} for ${p_item_object.price}', category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {purchased_item}!", category='danger')
        
        #sold item logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(item_obj=s_item_object):
                s_item_object.sell(user=current_user)
                flash(f'Congratulations! You sold {sold_item} back to market!', category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')

        return redirect(url_for('market_page'))
    else:
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template("market.html", items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


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
    




