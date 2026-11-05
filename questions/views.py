from django.shortcuts import render

def index(request):
    return render(request, "questions/index.html")


def hot(request):
    return render(request, "questions/hot.html")


def tag(request, tag_name):
    return render(request, "questions/tag.html", {"tag_name": tag_name})


def question(request, question_id):
    return render(request, "questions/question.html", {"question_id": question_id})


def ask(request):
    return render(request, "questions/ask.html")
