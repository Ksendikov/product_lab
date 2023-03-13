Установка:
1. Клонируем проект
2. Создаем у себя виртуальное окружение (заходим в него)
3. Бежим pip install -r requirements/dev.txt
4. Подключаем свою базу данных PostgreSQL в файле settings.py
5. Делаем миграции python manage.py migrate
6. Запускаем проект python manage.py runserver
