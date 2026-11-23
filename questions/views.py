from django.shortcuts import get_object_or_404, render

from core.utils import paginate

from .models import Answer, Question, Tag


def render_question_list(request, template, questions, **context):
    return render(request, template, {'page': paginate(questions, request), **context})


def index(request):
    return render_question_list(request, 'questions/index.html', Question.objects.newest())


def hot(request):
    return render_question_list(request, 'questions/hot.html', Question.objects.best())


def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    return render_question_list(
        request, 'questions/tag.html', Question.objects.by_tag(tag), tag_name=tag.name,
    )


def question(request, question_id):
    question = get_object_or_404(Question.objects.for_display(), pk=question_id)
    page = paginate(Answer.objects.for_question(question), request, per_page=5)
    return render(request, 'questions/question.html', {'question': question, 'page': page})


def ask(request):
    return render(request, 'questions/ask.html')