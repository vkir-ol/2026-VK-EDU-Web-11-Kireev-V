# AskPupkin
 
Проект по курсу Веб-технологии (VK Education). Сайт вопросов и ответов типа stackoverflow.
 
Киреев В., ИУ9, 2 курс
 
ДЗ1 - верстка лежит в папке public/
ДЗ2 - сделано на Django (views, urls, шаблоны, пагинация, docker)
 
## Запуск
 
Склонировать репозиторий:
```
git clone https://github.com/vkir-ol/2026-VK-EDU-Web-11-Kireev-V.git
cd 2026-VK-EDU-Web-11-Kireev-V
```
 
Скопировать .env.example в .env (там SECRET_KEY и другие настройки):
```
cp .env.example .env
```
(на windows: `copy .env.example .env`)
 
### Локально
 
```
python -m venv venv
venv\Scripts\activate          (на linux/mac: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
 
Открыть http://127.0.0.1:8000/
 
### Через Docker
 
```
docker compose up --build
```
 
Открыть http://localhost:8000/
 
## Страницы
 
- `/` - новые вопросы (index)
- `/hot/` - популярные вопросы (hot)
- `/tag/<tag>/` - вопросы по тегу (tag)
- `/question/<id>/` - вопрос и ответы (question)
- `/ask/` - создание вопроса (ask)
- `/login/` - вход (login)
- `/signup/` - регистрация (signup)
- `/profile/` - профиль (profile)

Пагинация через `?page=`, например `/?page=2`
 
## Структура
 
- application - настройки проекта
- core - вход, регистрация, профиль, base.html, статика, функция paginate
- questions - вопросы, ответы, теги
- public - верстка из ДЗ1