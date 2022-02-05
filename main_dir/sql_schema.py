from sqlalchemy import MetaData, create_engine
from sqlalchemy.exc import IntegrityError

from web_site.main_dir import db
from web_site.main_dir.db_models import Users

from faker import Faker
import sys
import random
import datetime

# Установить соединения между sqlalchemy и postgres dbapi
# Set up connections between sqlalchemy and postgres dbapi

engine = create_engine(
    "postgresql+psycopg2://postgres:1401@127.0.0.1:8000/work_project"
)
# Instantiate metadata class
# Создание экземпляра класса
metadata = MetaData()

# Создать экземпляр класса
# Instantiate faker class
faker = Faker()

# Отражение метаданных/схемы из существующей базы данных postgres
# Reflect metadata/schema from existing postgres database
with engine.connect() as conn:
    metadata.reflect(conn)

# создать табличные объекты
# create table objects
customers = metadata.tables.keys["customers"]
products = metadata.tables.keys["products"]
stores = metadata.tables.keys["stores"]
transactions = metadata.tables.keys["transactions"]

# populate_tables.py
...
# список поддельных товаров для вставки в таблицу товаров
# list of fake products to insert into the products table
product_list = ["hat", "cap", "shirt", "sweater", "sweatshirt",
                "shorts", "jeans", "sneakers", "boots", "coat", "accessories"]


class GenerateData:
    """
        generate a specific number of records to a target table in the
    postgres database.
        генерирует определенное количество записей в целевую таблицу в
    базе данных postgres.
    """

    def __init__(self):
        """
        define command line arguments.
        определяет аргументы командной строки
        """
        self.table = sys.argv[1]
        self.num_records = int(sys.argv[2])

    def create_data(self):
        """
        using the faker library, generate data and execute DML.
        с помощью библиотеки faker, сгенерировать данные и выполнить DML
        """

        if self.table not in metadata.tables.keys():
            return print(f"{self.table} does not exist")

        if self.table == "customers":
            ...
        if self.table == "products":
            ...
        if self.table == "stores":
            ...
        if self.table == "transactions":
            ...


if __name__ == "__main__":
    generate_data = GenerateData()
    generate_data.create_data()
