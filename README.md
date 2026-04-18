# cake-shop-demo-postgres

Демо-проект по заданию ДЭ 09.02.07-2-2026 для кондитерской **«Сладкий рай»**.

В репозитории есть:
- Django-приложение с авторизацией по ролям: гость, клиент, менеджер, администратор;
- PostgreSQL-конфигурация;
- SQL-скрипт создания базы;
- импорт товаров, пользователей, заказов и пунктов выдачи из Excel-файлов;
- CRUD для товаров и заказов;
- каталог товаров с поиском, фильтрацией и сортировкой;
- базовые шаблоны в стиле задания.

## Стек
- Python 3.12+
- Django
- PostgreSQL
- openpyxl

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### 1. Создать БД Postgres

```bash
psql -U postgres -f docs/init_db.sql
```

Либо вручную:

```sql
CREATE DATABASE cake_shop;
```

### 2. Применить миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Загрузить данные из приложений

```bash
python manage.py import_data
```

### 4. Запустить проект

```bash
python manage.py runserver
```

## Тестовые аккаунты
После импорта:
- Администратор: `kondratieva@cake-shop.ru` / `AdCk76#`
- Менеджер: `kremov@cake-shop.ru` / `Mn7@gP23`
- Клиент: `saharova.client@mail.ru` / `Cli3nt#9`

## Что сдавать
В ответ на экзамене можно прикрепить **ссылку на GitHub-репозиторий** с этим содержимым.

## Структура
- `shop/` — модели, формы, views, импорт данных
- `templates/` — HTML-шаблоны
- `static/` — стили и изображения
- `data/import/` — исходные Excel и картинки из задания
- `docs/init_db.sql` — SQL-скрипт создания БД
