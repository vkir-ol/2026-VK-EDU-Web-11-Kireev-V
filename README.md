# AskPupkin — статическая вёрстка (ДЗ1)
 
Учебный проект по курсу «Веб-технологии» (VK Education).
Сайт вопросов и ответов в духе Stack Overflow: пока только вёрстка.
 
**Автор:** Киреев В., студент 2 курса кафедры ИУ9, МГТУ им. Н. Э. Баумана.
 
## Как открыть
 
Сервер и сборка не нужны — это обычные HTML-файлы.
 
1. Склонировать репозиторий:
```bash
   git clone https://github.com/vkir-ol/2026-VK-EDU-Web-11-Kireev-V.git
```
2. Открыть файл `public/index.html` в браузере (двойной клик или перетащить в окно браузера).
Дальше по сайту можно ходить по ссылкам: логотип, вопросы, кнопка ASK!, log in / register, теги.

## Страницы

- **index** - `public/index.html` - список новых вопросов, лайки, пагинация
- **question** - `public/question.html` - страница вопроса ответы, форма ответа
- **ask** - `public/ask.html` - форма создания вопроса
- **login** - `public/login.html` - форма входа
- **signup** - `public/signup.html` - форма регистрации
- **profile** - `public/profile.html` - настройки профиля
- **base** - `public/base.html` - базовый шаблон: header, контент, sidebar и footer