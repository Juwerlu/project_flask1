Flask-приложение
=====
Данное приложение создано в рамках изучения Flask. Сайт занимается постоянным сбором новостей (Celery), отображает текущую погоду, а также имеет функционал регистрации/авторизации пользователей и комментирования постов.

Установка
---------
Создайте и активируйте виртуальное окружение, установите необходимые библиотеки:

    pip install -r requirements.txt

Настройка
---------
Создайте файл config.py, добавьте следующие настройки:

    import os

    from datetime import timedelta

    basedir = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
    WEATHER_DEFAULT_CITY = 'CITY,COUNTRY'
    WEATHER_API_KEY = 'API_KEY'
    WEATHER_URL = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'

    SECRET_KEY = 'SECRET_KEY'
    REMEMBER_COOKIE_DURATION = timedelta(days=30)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
Создайте исполняемый скрипт:

    chmod +x run.sh

Запуск
-------

В активированном виртуальном окружении введите:

    ./run.sh
