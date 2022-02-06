from werkzeug.security import generate_password_hash

from Flask_Project.app.db_models import User


def admin():
    site_admin = User(
        age=100,
        nickname='admin',
        password=generate_password_hash('admin'),
        email='admin@gmail.com',
        is_admin=True,
    )

    return site_admin
