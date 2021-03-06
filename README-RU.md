<h1><div align="center">РискАналитик</div></h1>

# Обзор
Веб-сайт обладает следующими возможностями:
- поиск судебных дел с помощью различных фильтров: категория, требования, обстоятельство и решение;
- просмотр иерархии дела;
- открытие текста отдельного документа дела;
- просмотр характеристики дела (категорию спора, требования, обстоятельства, решение по делу в целом, решение на данной инстанции);
- просмотр статистики решений по выбранным фильтрам с помощью круговой диаграммы;
- просмотр по выбранным фильтрам количества дел, завершившихся на каждой из инстанций, с помощью гистограммы.
# Как начать
1. Клонируйте репозиторий в вашу папку.
2. Установите все зависимости (requirements.txt).
3. Создайте БД в PostgreSQL (pgAdmin 4).
4. Настройте подключение к БД в файле ```__init__.py``` по шаблону:  
```app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@server/db'```
5. Запустите проект.
# Использование
Ознакомиться с сайтом можно по следующей ссылке:
[https://frit027.pythonanywhere.com/]()
# Технологии
## Backend
1. Python 3.8
2. Flask
3. PostgreSQL (ORM: Flask-SQLAlchemy)
## Frontend
1. JavaScript (jQuery)
2. HTML5 (Jinja2)
3. CSS3