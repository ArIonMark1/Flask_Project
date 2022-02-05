from werkzeug.security import generate_password_hash

from web_site.main_dir.db_models import Users


def admin():
    admin = Users(
        first_name=None,
        last_name=None,
        age=100,
        nickname='admin',
        password=generate_password_hash('admin'),
        email='admin@gmail.com',
        is_admin=True,
    )
    return admin
