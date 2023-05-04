
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from renovering import db, bcrypt
from renovering.models import User, Post
from renovering.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from renovering.users.utils import save_picture, send_reset_email

# denna är alltså registrerad i __init__.py
users = Blueprint('users', '__name__')

@users.route('/register', methods =['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect (url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Kontot skapades, vänligen logga in', 'success')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods =['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect (url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # få nästa parameter (URL)

            return redirect(next_page) if next_page else  redirect(url_for('main.home'))
        else:
            flash('Kunde tyvärr inte logga in, vänligen kontrollera användarnamn och lösenord', 'danger')

    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods =['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data 
        current_user.email = form.email.data 
        db.session.commit()
        flash('Ditt konto har uppdaterats', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email 

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # default bilden.
    return render_template('Account.html', title='Account', 
                           image_file=image_file, form=form)



@users.route('/user/<string:username>')
def user_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404

    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)



@users.route('/reset_password',methods =['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Ett epostmeddelande med information om hur du återställer lösenordet har skickats.', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Återställ lösenord', form=form)


@users.route('/reset_password/<token>',methods =['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Token är felaktigt eller utgånget!', 'warning')
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        User.password = hashed_password
        db.session.commit()

        flash('Ditt lösenord har ändrats', 'success')
        return redirect(url_for('users.login'))
    
    return render_template('reset_token.html', title='Återställ lösenord.', form=form)