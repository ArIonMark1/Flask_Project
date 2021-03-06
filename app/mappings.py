import datetime
import json
import os.path
from pathlib import Path

from flask import render_template, url_for, request, flash, redirect, session, abort, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from Flask_Project.app.app import app, db
from Flask_Project.app.db_models import User
from Flask_Project.app.data_insertion import FillBase
from Flask_Project.app.seeds.seed_database import create_fake_users

app_dir = Path(__file__).parent
json_path = os.path.join(app_dir, 'seeds/data_db.json')  # путь к файлу json, для загрузки-выгрузки данных

# db.session.query(User).delete()
# db.session.commit()

# -----------------------------------------------
if not db.session.query(User).all():
    """ Автоматическое создание админ-странички для разработчика """
    print('База пустая')

    admin_create = {
        'first_name': 'admin',
        'last_name': 'admin',
        'age': 100,
        'nickname': 'admin',
        'password': generate_password_hash('admin'),
        'email': 'admin@gmail.com',
        'is_admin': True,
        'description': '',
        'last_login': '2022-01-28 08:27:51'
    }
    """ Передаем параметры для регистрации пользователя, сессию и таблицу базы данных """
    admin = FillBase(User, admin_create, db.session).create_user()

    print(f'Created Superuser: nick: "admin", pass: "admin"')


elif db.session.query(User).count() and db.session.query(User).count() < 100:
    """ Если админ был создан - создается нужное количество пользователей 
    и записывается в базу данных( пример работы с json файлами)"""

    with open(json_path, 'w', encoding='utf-8') as file:
        """ Создание пользователей """
        file.write(json.dumps(create_fake_users(10), sort_keys=True, ensure_ascii=False))


    def load_json_data():
        with open(json_path, encoding='utf-8') as j_file:
            return json.load(j_file)


    for user_data in load_json_data():
        try:
            """ Так как никнейм должен быть уникальным - проверяем, если такой есть уже есть игнорируем добавление """
            create_user = FillBase(User, user_data, db.session).create_user()
        except Exception:
            print(f'Dublicate nickname {user_data["nickname"]}')
            pass

    print(db.session.query(User).count())

else:
    print('database is full')


# -----------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def login_page():
    """ Страница входа зарегистрированного пользователя """
    if current_user.is_authenticated:

        return redirect(url_for('user_work_page', u_id=current_user.id))

    elif request.method == 'POST':
        nickname = request.form.get('nickname')
        password = request.form.get('password')

        if nickname and password:
            """ Проверяем если форма не пустая проверяем есть ли пользователь с этими данными """
            user = db.session.query(User).filter(User.nickname == nickname).first()

            if user and check_password_hash(user.password, password):
                # Передаем подтвержденного пользователя в логин-менеджер
                login_user(user)
                # Записываем время входа в систему
                user.last_login = datetime.datetime.now()
                db.session.add(user)
                db.session.commit()

                return redirect(url_for('user_work_page', u_id=user.id))
            else:
                flash('Login or Password is not correct.')
        else:
            flash('Please fill Login and Password fields.')

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
            flash('Please fill all fields.')
        elif password != password2:
            flash('Passwords  are not equal.')
        elif email and db.session.query(User).filter(User.email == email).first():
            flash('Wrong Email address, try again.')
        else:
            hash_key = generate_password_hash(password)
            new_user = User(
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
            """ После успешной регистрации перенаправляет нового пользователя на страницу входа """
            return redirect(url_for('login_page'))
    # рендеринг страницы регистрации
    return render_template('register.html', title='User Registration')


@app.route(f'/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_page(user_id):
    """ Страница редактирования пользователя """
    selected_user = db.session.query(User).filter(User.id == user_id)
    if selected_user.count():
        user = selected_user.first()

        if request.method == 'POST':

            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.age = request.form['age']
            user.nickname = request.form['nickname']
            user.email = request.form['email']
            user.description = request.form['description']
            # обработка поля админа,  если текущий пользователь админ - может редактировать поле, иначе просто отображение статуса
            if current_user.is_admin and request.form['is_admin'] == 'True':

                print(request.form['is_admin'])
                user.is_admin = True
            else:
                user.is_admin = False

            db.session.add(user)
            db.session.commit()
            # После завершения редактирования пользователя, перенаправляет в кабинет пользователя
            return redirect(url_for('user_work_page', u_id=current_user.id))
        else:
            # При GET запросе отображает страницу с данными выбранного пользователя
            content = dict(
                title=f'{user.nickname.upper()} page',
                context=f'{user.nickname.upper()} user edit page ',
                user=user
            )
            return render_template('current_user_page.html', **content)

    else:
        # В случае если id запрашиваемого пользователя нету в базе - возвращает страницу-ошибку: страница не найдена
        abort(404)


@app.route(f'/user/<int:u_id>')
@login_required
def user_work_page(u_id):
    """Рабочая страница, кабинет зарегистрированного пользователя, список всех пользователей """

    if '_user_id' not in session or int(session['_user_id']) != u_id:
        """ Проверка на активность пользователя, залогинен ли пользователь в системе """
        abort(404)

    else:
        logged_user = db.session.query(User).filter(User.id == u_id).first()

        content = dict(
            title='User work page',
            context=f'Welcome back user {logged_user.nickname.upper()}',
            users=db.session.query(User).all()

        )
        return render_template('user_work_page.html', **content)


@app.route('/user/delete/confirm_delete/<int:user_id>/<string:control>')
@app.route('/user/delete/<int:user_id>')
def delete_user(user_id, control=None):
    """ Удаление пользователя """
    print(user_id)
    victim_user = db.session.query(User).filter(User.id == user_id)

    if victim_user.count() and not control:  # Страница подтверждения удаления
        user = victim_user.first()
        return render_template('user_confirm_delete.html', user=user)
        # ###########################################################
    elif victim_user.count() and control:
        # Обработка варриантов выбора пользователя
        if control == 'True':
            # Если пользователь подтвердил удаление перенаправляем его на страничку входа
            # во избежания ошибки, если пользователь удалил самого себя
            victim_user.delete()
            db.session.commit()
            return redirect(url_for('login_page'))

        return redirect((url_for('user_page', user_id=user_id)))


@app.errorhandler(404)
def page_not_found(err):
    """ Обработка несуществующей страницы """
    return render_template('page_404.html', title='Page not found')


@app.route('/logout')
def logout():
    """ Выход пользователя """
    logout_user()
    return redirect(url_for('login_page'))
