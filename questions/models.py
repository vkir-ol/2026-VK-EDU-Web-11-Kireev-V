from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


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
    rating = models.IntegerField(default=0, db_index=True, verbose_name='Рейтинг')
    created_at = models.DateTimeField(default=timezone.now, db_index=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.title


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
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
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