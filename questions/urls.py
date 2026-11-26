from django.urls import path

from . import views
from .models import Answer, Question

urlpatterns = [
    path("", views.index, name="index"),
    path("hot/", views.hot, name="hot"),
    path("tag/<path:tag_name>/", views.tag, name="tag"),
    path("question/<int:question_id>/", views.question, name="question"),
    path("ask/", views.ask, name="ask"),
    path('question/<int:object_id>/vote/', views.vote, {'model': Question}, name='question_vote'),
    path('answer/<int:object_id>/vote/', views.vote, {'model': Answer}, name='answer_vote'),
    path('question/<int:question_id>/correct/', views.mark_correct, name='mark_correct'),
]