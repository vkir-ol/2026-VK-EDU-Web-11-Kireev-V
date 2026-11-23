from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models import Count, OuterRef, Subquery, Sum, Value
from django.db.models.functions import Coalesce
from django.urls import reverse

def related_total(queryset, foreign_key, aggregate):
    totals = queryset.filter(**{foreign_key: OuterRef('pk')}).order_by()
    totals = totals.values(foreign_key).annotate(total=aggregate).values('total')
    return Coalesce(Subquery(totals), Value(0), output_field=models.IntegerField())


class TagManager(models.Manager):
    def popular(self):
        return self.annotate(question_count=Count('questions')).filter(
            question_count__gt=0,
        ).order_by('-question_count', 'name')[:5]


class QuestionManager(models.Manager):
    def for_display(self):
        return self.select_related('author__profile').prefetch_related('tags').annotate(
            rating=related_total(QuestionLike.objects, 'question_id', Sum('value')),
        )

    def newest(self):
        return self.for_display().annotate(
            answers_count=related_total(Answer.objects, 'question_id', Count('*')),
        ).order_by('-created_at', '-pk')

    def best(self):
        return self.newest().order_by('-rating', '-created_at', '-pk')

    def by_tag(self, tag):
        return self.newest().filter(tags=tag)


class AnswerManager(models.Manager):
    def for_question(self, question):
        return self.filter(question=question).select_related('author__profile').annotate(
            rating=related_total(AnswerLike.objects, 'answer_id', Sum('value')),
        ).order_by('-is_correct', 'created_at', 'pk')
 
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Название')
    objects = TagManager()

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', args=[self.name])


class Question(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Автор',
    )
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True, verbose_name='Теги')
    objects = QuestionManager()
    created_at = models.DateTimeField(default=timezone.now, db_index=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question', args=[self.pk])


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Автор',
    )
    text = models.TextField(verbose_name='Текст')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')
    objects = AnswerManager()
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f'Ответ #{self.id} к вопросу #{self.question_id}'


LIKE_CHOICES = [
    (1, 'Лайк'),
    (-1, 'Дизлайк'),
]


class QuestionLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='question_likes',
        verbose_name='Пользователь',
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Вопрос',
    )
    value = models.SmallIntegerField(choices=LIKE_CHOICES, verbose_name='Оценка')

    class Meta:
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'
        unique_together = ('user', 'question')

    def __str__(self):
        return f'{self.user} → вопрос #{self.question_id}: {self.value}'


class AnswerLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answer_likes',
        verbose_name='Пользователь',
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Ответ',
    )
    value = models.SmallIntegerField(choices=LIKE_CHOICES, verbose_name='Оценка')

    class Meta:
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'
        unique_together = ('user', 'answer')

    def __str__(self):
        return f'{self.user} → ответ #{self.answer_id}: {self.value}'