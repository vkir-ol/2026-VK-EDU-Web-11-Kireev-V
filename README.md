# AskPupkin

Проект по курсу Веб-технологии (VK Education). Сайт вопросов и ответов типа stackoverflow.

Киреев В., ИУ9, 2 курс

- ДЗ1 - статическая верстка (ветка hw-1)
- ДЗ2 - сделано на Django (views, urls, шаблоны, пагинация, docker)
- ДЗ3 - добавлены модели, PostgreSQL, админка и тестовые данные. Вопросы и ответы выводятся из базы.

## Запуск

Склонировать репозиторий и перейти на ветку ДЗ3:

```
git clone https://github.com/vkir-ol/2026-VK-EDU-Web-11-Kireev-V.git
cd 2026-VK-EDU-Web-11-Kireev-V
git switch hw-3
```

### Локально

Нужны Python 3.12 и запущенный PostgreSQL.

Скопировать `.env.example` в `.env.local`. В PowerShell:

```powershell
Copy-Item .env.example .env.local
```

Заполнить `DJANGO_SECRET_KEY` и `POSTGRES_PASSWORD`. Для локальной базы оставить `POSTGRES_HOST=127.0.0.1` и `POSTGRES_PORT=5432`.

Для первого запуска создать пользователя и базу в `psql` под администратором PostgreSQL:

```sql
CREATE ROLE askpupkin LOGIN;
\password askpupkin
CREATE DATABASE askpupkin OWNER askpupkin;
```

На запрос `\password` ввести пароль из `POSTGRES_PASSWORD` в `.env.local`.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8001
```

На Linux/macOS активировать окружение через `source venv/bin/activate`.

Открыть [http://127.0.0.1:8001/](http://127.0.0.1:8001/).

### Через Docker

Скопировать `.env.example` в `.env.docker`, заполнить ключ Django и пароль базы, поставить `POSTGRES_HOST=db`.

```powershell
docker compose --env-file .env.docker up --build -d
docker compose --env-file .env.docker exec web python manage.py createsuperuser
```

Django ждёт запуска PostgreSQL и применяет миграции. Данные базы хранятся в томе `postgres_data`.

Открыть [http://localhost:8000/](http://localhost:8000/). Чтобы открыть сайт на порту `8002`, указать `DJANGO_HOST_PORT=8002` в `.env.docker`.

### Тестовые данные

Для небольшой проверки запустить:

```powershell
python manage.py fill_db 2
```

Для базы в Docker:

```powershell
docker compose --env-file .env.docker exec web python manage.py fill_db 2
```

Коэффициент `ratio` задаёт количество пользователей, профилей и тегов. Вопросов будет `ratio * 10`, ответов `ratio * 100`, оценок `ratio * 200`. Минимальный `ratio` — `2`, для проверки большого объёма можно запустить `fill_db 10000`.

## Страницы

- `/` - новые вопросы (index)
- `/hot/` - популярные вопросы (hot)
- `/tag/<tag>/` - вопросы по тегу (tag)
- `/question/<id>/` - вопрос и ответы (question)
- `/ask/` - форма создания вопроса (ask)
- `/login/` - вход (login)
- `/signup/` - регистрация (signup)
- `/profile/` - профиль (profile)
- `/admin/` - админка

Пагинация через `?page=`, например `/?page=2`.

При `DJANGO_DEBUG=True` можно посмотреть SQL-запросы через Django Debug Toolbar.

## Структура

- application - настройки проекта
- core - вход, регистрация, профиль, base.html, статика, функция paginate
- questions - вопросы, ответы, теги, оценки и команда fill_db