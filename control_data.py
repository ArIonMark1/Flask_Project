import os
from pathlib import Path
from pprint import pprint

import psycopg2
from dotenv import load_dotenv

load_dotenv()
env_path = Path(__file__).parents[0] / '.env'
load_dotenv(dotenv_path=env_path)

conn = None
try:
    print(env_path)
    print('Connect to the PostgreSQL database...')

    conn = psycopg2.connect(
        host=os.getenv('HOST'),
        port=os.getenv('PORT'),
        database=os.getenv('DATABASE'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
    )

    cur = conn.cursor()

    print('PostgreSQL database:')
    cur.execute('SELECT version()')

    db_version = cur.fetchone()
    print('Version: ', db_version)
    # ------------------------------------------
    cur.execute('SELECT id, nickname, age FROM users LIMIT 5;')
    res = cur.fetchall()
    print('Первые 5 пользователей зарегистрированых в базе:')
    pprint(res)
    # ------------------------------------------
    cur.execute(
        "SELECT id, first_name, last_name FROM users WHERE last_login between '2022-01-01 17:29:54' AND '2022-01-30 17:29:54' ")
    res = cur.fetchall()
    print('Выборка пользователей за январь текущего года:')
    pprint(res)
    # ------------------------------------------
    cur.execute(" SELECT count(id) FROM users WHERE age between '25' AND '50' ")
    res = cur.fetchall()
    print('Общее количество пользователей в возрастном диапазоне от 25 до 50:')
    pprint(res)
    # ------------------------------------------
    cur.execute("SELECT id, age, "
                "CASE "
                "WHEN age > 50 THEN 'older' "
                "WHEN age < 25 THEN 'young' "
                "ELSE 'adult' "
                "END "
                "FROM users "
                "ORDER BY age; ")
    res = cur.fetchall()
    print('Распределение пользователей по возрасту, меньше 25 - молодые, больше 50 - пожилые, между - взрослые.')
    pprint(res)
    # ------------------------------------------
    cur.execute(" SELECT id, nickname FROM users WHERE is_admin=TRUE;")
    res = cur.fetchall()
    print(' Админы в базе:')
    pprint(res)
    # ------------------------------------------
    cur.close()

except(Exception, psycopg2.DatabaseError) as err:
    print(err)

finally:
    if conn is not None:
        conn.close()
        print('Database connection closed.')
