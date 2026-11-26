from django.shortcuts import get_object_or_404, render, redirect
from core.utils import paginate
from .models import Answer, Question, Tag
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import JsonResponse

from .forms import QuestionForm, AnswerForm, VoteForm, CorrectAnswerForm



def render_question_list(request, template, questions, **context):
    return render(request, template, {'page': paginate(questions, request, per_page=20), **context})


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
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path())

    form = AnswerForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        answer = form.save(author=request.user, question=question)
        return redirect(answer)

    page = paginate(Answer.objects.for_question(question), request, per_page=Answer.PAGE_SIZE)
    return render(request, 'questions/question.html', {
        'question': question,
        'page': page,
        'form': form,
    })


@login_required
def ask(request):
    form = QuestionForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        question = form.save(author=request.user)
        return redirect(question)
    return render(request, 'questions/ask.html', {'form': form})



def vote(request, object_id, model):
    if request.method != 'POST':
        response = JsonResponse({'error': 'Нужен POST-запрос.'}, status=405)
        response['Allow'] = 'POST'
        return response

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Войдите, чтобы голосовать.'}, status=401)

    form = VoteForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': 'Оценка должна быть +1 или −1.'}, status=400)

    try:
        rating = form.save(model=model, object_id=object_id, user=request.user)
    except model.DoesNotExist:
        return JsonResponse({'error': 'Объект не найден.'}, status=404)
    except ValidationError as exc:
        return JsonResponse({'error': exc.messages[0]}, status=409)

    return JsonResponse({'rating': rating})


def mark_correct(request, question_id):
    if request.method != 'POST':
        response = JsonResponse({'error': 'Нужен POST-запрос.'}, status=405)
        response['Allow'] = 'POST'
        return response

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Войдите, чтобы выбрать ответ.'}, status=401)

    form = CorrectAnswerForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error': 'Некорректный ID ответа.'}, status=400)

    try:
        answer = form.save(question_id=question_id, user=request.user)
    except PermissionDenied as exc:
        return JsonResponse({'error': str(exc)}, status=403)
    except (Question.DoesNotExist, Answer.DoesNotExist):
        return JsonResponse({'error': 'Вопрос или ответ не найден.'}, status=404)

    return JsonResponse({
        'answer_id': answer.pk,
        'is_correct': answer.is_correct,
        'url': answer.get_absolute_url(),
    })