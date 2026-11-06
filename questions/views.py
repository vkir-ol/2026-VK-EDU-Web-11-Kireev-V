from django.http import Http404
from django.shortcuts import render
from core.utils import paginate

TAGS = ["python", "django", "football", "MySQL", "perl"]

TITLES = [
    "How to play football like Cristiano Ronaldo?",
    "Why does my Django migration fail?",
    "Is MySQL faster than PostgreSQL?",
    "How to center a div with Bootstrap?",
    "What is the best way to learn Python?",
]

QUESTIONS = []
for i in range(1, 51):
    QUESTIONS.append({
        "id": i,
        "title": f"{TITLES[i % len(TITLES)]} (#{i})",
        "text": f"Question text {i}. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, "
                f"sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.",
        "tags": [TAGS[i % len(TAGS)], TAGS[(i + 2) % len(TAGS)]],
        "answers_count": 5 + i % 10,
        "rating": i * 7 % 25 - 5,
        "vote": [None, "up", "down"][i % 3],
        "avatar": f"core/img/avatar-{i % 3 + 1}.png",
        "created": f"{i} hours ago",
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
    if question_id < 1 or question_id > len(QUESTIONS):
        raise Http404("Вопрос не найден")

    question = QUESTIONS[question_id - 1]

    answers = []
    for i in range(1, question["answers_count"] + 1):
        answers.append({
            "id": i,
            "text": f"Answer {i}. First of all I would like to thank you for the invitation to participate in such a great discussion. Lorem ipsum dolor sit amet.",
            "rating": 10 - i,
            "vote": "up" if i == 1 else None,
            "avatar": f"core/img/avatar-{i % 3 + 1}.png",
            "created": f"{i * 10} minutes ago",
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
