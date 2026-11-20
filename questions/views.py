from django.http import Http404
from django.shortcuts import render
from core.utils import paginate

TAGS = ["python", "django", "football", "MySQL", "perl"]

TITLES = [
    "Как играть в футбол как Криштиану Роналду?",
    "Почему падает миграция в Django?",
    "MySQL быстрее, чем PostgreSQL?",
    "Как отцентрировать блок в Bootstrap?",
    "Как лучше всего выучить Python?",
]

AVATARS = [
    "core/img/avatar-1.png",
    "core/img/avatar-2.jpg",
    "core/img/avatar-3.png",
    "core/img/avatar-4.jpg",
]

QUESTIONS = []
for i in range(1, 51):
    QUESTIONS.append({
        "id": i,
        "title": f"{TITLES[i % len(TITLES)]} (#{i})",
        "text": f"Текст вопроса {i}. Здесь подробно описана проблема: что уже пробовал и что не получилось.",
        "tags": [TAGS[i % len(TAGS)], TAGS[(i + 2) % len(TAGS)]],
        "answers_count": 5 + i % 10,
        "rating": i * 7 % 25 - 5,
        "vote": [None, "up", "down"][i % 3],
        "avatar": AVATARS[i % len(AVATARS)],
        "created": f"{i} ч. назад",
    })



def index(request):
    page = paginate(QUESTIONS, request)
    return render(request, "questions/index.html", {"page": page})

def hot(request):
    hot_questions = sorted(QUESTIONS, key=lambda q: q["rating"], reverse=True)
    page = paginate(hot_questions, request)
    return render(request, "questions/hot.html", {"page": page})

def tag(request, tag_name):
    tagged = [q for q in QUESTIONS if tag_name in q["tags"]]
    page = paginate(tagged, request)
    return render(request, "questions/tag.html", {"tag_name": tag_name, "page": page})

def question(request, question_id):
    question = None
    for q in QUESTIONS:
        if q["id"] == question_id:
            question = q
            break

    if question is None:
        raise Http404("Вопрос не найден")

    answers = []
    for i in range(1, question["answers_count"] + 1):
        answers.append({
            "id": i,
            "text": f"Ответ {i}. Спасибо за вопрос! Попробуй начать с простого и разобраться по шагам.",
            "rating": 10 - i,
            "vote": "up" if i == 1 else None,
            "avatar": AVATARS[i % len(AVATARS)],
            "created": f"{i * 10} мин. назад",
            "is_correct": i == 1,
        })

    page = paginate(answers, request, 5)
    return render(request, "questions/question.html", {
        "question": question,
        "answers_count": len(answers),
        "page": page,
    })

def ask(request):
    return render(request, "questions/ask.html")
