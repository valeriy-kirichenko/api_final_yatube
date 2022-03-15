API YaTube 
=====

Описание проекта
----------
API для проекта Yatube. Аутентификация осуществляется по JWT-токену.
Реализованы пагинация ответов, поиск, фильтрация.

Системные требования
----------
* Python 3.9+
* Works on Linux, Windows, macOS, BSD

Стек технологий
----------
* Python 3.9
* Django 2.2 
* Django Rest Framework
* Pytest
* Simple-JWT
* SQLite3

Установка проекта из репозитория (Windows)
----------

1. Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone 'git@github.com:valeriy-kirichenko/api_final_yatube.git'

cd api_final_yatube
```
2. Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv env

source env/Scripts/activate
```
3. Установить зависимости из файла ```requirements.txt```:
```bash
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```
4. Выполнить миграции:
```bash
cd yatube_api

python3 manage.py migrate
```
5. Запустить проект (в режиме сервера Django):
```bash
python3 manage.py runserver
```
Документация к проекту с примерами запросов и ответов
----------
Документация для API [доступна по ссылке](http://localhost:8000/redoc/) после установки приложения.
