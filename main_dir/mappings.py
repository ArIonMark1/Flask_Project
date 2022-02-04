import datetime

from flask import Flask, render_template, url_for, request, flash, redirect, session, abort, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from web_site.main_dir import app, db
from web_site.main_dir.db_models import Users


@app.route('/', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:

        return redirect(url_for('user_work_page', u_id=current_user.id))

    elif request.method == 'POST':
        nickname = request.form.get('nickname')
        password = request.form.get('password')

        if nickname and password:
            user = db.session.query(Users).filter(Users.nickname == nickname).first()

            if user and check_password_hash(user.password, password):
                login_user(user)

                user.last_login = datetime.datetime.now()
                db.session.add(user)
                db.session.commit()

                return redirect(url_for('user_work_page', u_id=user.id))
            else:
                flash('Login or Password is not correct!')
        else:
            flash('Please fill Login and Password fields!')

    return render_template('login.html', title='Login Page')


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
        elif email and db.session.query(Users).filter(Users.email == email).first():
            flash('Wrong Email address, try again!!')
        else:
            hash_key = generate_password_hash(password)
            new_user = Users(
                first_name=first_name,
                last_name=last_name,
                age=age,
                nickname=nickname,
                password=hash_key,
                email=email,
                description=description,
                is_admin=False
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Registration completed successfully')
            return redirect(url_for('login_page'))

    return render_template('register.html', title='User Registration')


@app.route(f'/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_page(user_id):
    """ Страница редактирования пользователя """
    selected_user = db.session.query(Users).filter(Users.id == user_id)
    if selected_user.count():
        user = selected_user.first()

        if request.method == 'POST':

            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.age = request.form['age']
            user.nickname = request.form['nickname']
            user.email = request.form['email']
            user.description = request.form['description']
            if request.form['is_admin'] == 'True':
                user.is_admin = True

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('user_work_page', u_id=current_user.id))
        else:
            content = dict(
                title=f'{user.nickname.upper()} page',
                context=f'{user.nickname.upper()} user edit page ',
                user=user
            )
            return render_template('current_user_page.html', **content)

    else:
        abort(404)


@app.route(f'/user/<int:u_id>')
@login_required
def user_work_page(u_id):
    """Рабочая страница зарегистрированого пользователя, список всех пользователей """

    if '_user_id' not in session or int(session['_user_id']) != u_id:
        """ Проверка на активность пользователя, залогинен ли пользователь в системе """
        abort(404)

    else:
        logged_user = db.session.query(Users).filter(Users.id == u_id).first()

        content = dict(
            title='User work page',
            context=f'Welcome back user {logged_user.nickname.upper()}',
            users=db.session.query(Users).all()

        )
        return render_template('user_work_page.html', **content)


@app.route('/user/delete/confirm_delete/<int:user_id>/<string:control>')
@app.route('/user/delete/<int:user_id>')
def delete_user(user_id, control=None):
    """ Удаление пользователя """
    print(user_id)
    victim_user = db.session.query(Users).filter(Users.id == user_id)

    if victim_user.count() and not control:  # Страница подтверждения удаления
        user = victim_user.first()
        return render_template('user_confirm_delete.html', user=user)
        # ###########################################################
    elif victim_user.count() and control:

        if control == 'True':
            victim_user.delete()
            db.session.commit()
            return redirect(url_for('user_work_page', u_id=current_user.id))

        return redirect((url_for('user_page', user_id=user_id)))


@app.errorhandler(404)
def page_not_found(error):
    """ Обработка несуществующей страницы """
    return render_template('page_404.html', title='Page not found')


@app.route('/logout')
def logout():
    """ Выход пользователя """
    logout_user()
    return redirect(url_for('login_page'))
