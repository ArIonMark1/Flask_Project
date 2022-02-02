import datetime

from flask import Flask, render_template, url_for, request, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

from web_site.main_dir import app, db
from web_site.main_dir.db_models import Users


@app.route('/', methods=['GET', 'POST'])
def login_page():
    nickname = request.form.get('nickname')
    password = request.form.get('password')

    if request.method == 'POST':

        if nickname and password:
            user = db.session.query(Users).filter(Users.nickname == nickname).first()

            if user and check_password_hash(user.password, password):
                login_user(user)

                return redirect(url_for('user_page', u_id=user.id))
            else:
                flash('Login or Password is not correct!')
        else:
            flash('Please fill Login and Password fields!')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """ Регистрация нового пользователя """
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    age = request.form.get('age')
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    email = request.form.get('email')
    description = request.form.get('description')

    if request.method == 'POST':
        if not (nickname or password or password2 or email):
            flash('Please fill all fields!!')
        elif password != password2:
            flash('Passwords  are not equal!!')
        else:
            hash_key = str(generate_password_hash(password))
            new_user = Users(
                first_name=first_name,
                last_name=last_name,
                age=age,
                nickname=nickname,
                password=hash_key,
                email=email,
                description=description,
                last_login=datetime.datetime.now()
            )
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route(f'/user/<int:u_id>')
def user_page(u_id):
    logged_user = db.session.query(Users).filter(Users.id == u_id).first()
    content = dict(
        title='User page',
        context=f'Welcome back user {logged_user.nickname.upper()}',
        users=db.session.query(Users).all()
    )
    return render_template('user_page.html', **content)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))
