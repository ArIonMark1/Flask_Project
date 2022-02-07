from Flask_Project.app.app import app
# from app.seeds.sql_schema import DemoSeeder

# Точка старта проекта
# from Flask_Project.app.db_models import DemoSeeder

if __name__ == '__main__':
    # demo = DemoSeeder()
    # demo.run()
    app.run(debug=True)
