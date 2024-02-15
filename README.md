# Food_app

[![python](https://img.shields.io/badge/python-3.10_-blue?style=flat-square)](https://www.python.org/)
[![fastapi](https://img.shields.io/badge/fastapi-0.109.0-critical?style=flat-square)](https://fastapi.tiangolo.com/)
[![pytest](https://img.shields.io/badge/pytest-passed-brightgreen)](https://docs.pytest.org/en/7.4.x/)
[![sqlalchemy](https://img.shields.io/badge/sqlalchemy-2.0.25-critical?style=flat-square)](https://www.sqlalchemy.org//)
[![alembic](https://img.shields.io/badge/alembic-1.13.1_-violet?style=flat-square)](https://alembic.sqlalchemy.org//)


## Описание

<details>
<summary><b>ЗАДАНИЯ:</b></summary>

1. Проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте реализовано REST API по работе с меню ресторана, все CRUD операции. Даны 3 сущности: Меню, Подменю, Блюдо.

    Зависимости:
    - У меню есть подменю, которые к ней привязаны.
    - У подменю есть блюда.

    Реализовано:
    - Блюдо не может быть привязано напрямую к меню, минуя подменю.
    - Блюдо не может находиться в 2-х подменю одновременно.
    - Подменю не может находиться в 2-х меню одновременно.
    - Если удалить меню, должны удалиться все подменю и блюда этого меню.
    - Если удалить подменю, должны удалиться все блюда этого подменю.
    - Цены блюд выводить с округлением до 2 знаков после запятой.
    - Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.
    - Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.
    - Вынести бизнес логику и запросы в БД в отдельные слои приложения.
    - Добавить кэширование запросов к API  с использованием Redis. Не забыть про инвалидацию кэша.
    - Добавить pre-commit хуки в проект.
    - Покрыть проект type hints (тайпхинтами)
    - Описать ручки API в соответствий c OpenAPI
    - Реализовать в тестах аналог Django reverse() для FastAPI
    - Контейнеры с проектом и с тестами запускаются разными командами.
    - Добавить эндпоинт (GET) для вывода всех меню со всеми связанными подменю и со всеми связанными блюдами.(api/v1/menu/views 143 строчка)
    - Реализовать инвалидация кэша в background task (встроено в FastAPI)

</details>


## Для запуска проекта

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/timmashkov/ylab_tasks.git
```

```
cd food_app
```
Настроить переменные окружения:
```
исправте файл .env либо работайте с указанными данными
```

#### Основной docker-compose командой "docker compose up --build"
#### Тестовый docker-compose командой "docker compose -f docker-compose-test.yaml up --build". После прохождения ввести
в консоль Ctrl+c для остановки контейнера

## Локальный запуск

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```
Поднять локально Redis

Выполнить миграции:

```
alembic upgrade head
```
Не забудьте поднять редис и рэббит перед тестами!
Прогнать тесты:
```
pytest .\tests -v
```

Запустить проект:

```
uvicorn runner:app --reload
или запустить runner.py
```
Запустить сваггер:
```
http://127.0.0.1:8000/docs
```
