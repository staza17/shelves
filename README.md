# Shelves
Shelves - это сервис для создания онлайн-досок, использующих метод канбан для структурирования идей и управления проектами.

Пользователь создает доски, разделенные на три колонки, создает внутри карточки с текстом и перемещает их между колонками.

Проект использует Flask и базу данных SQLAlchemy.

## Установка

Клонируйте репозиторий на свой компьютер, создайте виртуальное окружение и установите зависимости:

```
git clone https://github.com/staza17/shelves.git
python3 -m venv env
env\Script\activate
pip install -r requirements.txt
```

## Настройка

Создайте файл config.py в папке webapp и добавьте туда настройки:

```
SQLALCHEMY_DATABASE_URI = "Ссылка на вашу базу данных"

SECRET_KEY = "Введите случайный набор латинских символов"

REMEMBER_COOKIE_DURATION = timedelta(days=5)

SQLALCHEMY_TRACK_MODIFICATIONS = False
```

Чтобы создать базу данных, введите в консоли:

```
python create_db.py
```

Создайте админа:

```
python create_admin.py
```

Введите логин и пароль.

## Запуск

Чтобы запустить проект, введите в консоли:

```
run
```