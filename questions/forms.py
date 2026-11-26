from django import forms
from django.db import transaction
from django.db.models import Sum
from django.core.exceptions import PermissionDenied

from .models import Question, Tag, Answer, LIKE_CHOICES


class QuestionForm(forms.ModelForm):
    text = forms.CharField(
        label='Текст вопроса',
        max_length=5000,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
    )
    tag_names = forms.CharField(
        label='Теги',
        required=False,
        max_length=100,
        help_text='Через запятую, до 3 тегов, каждый не длиннее 20 символов.',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Question
        fields = ('title', 'text', 'tag_names')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_tag_names(self):
        names = []
        for part in self.cleaned_data['tag_names'].split(','):
            name = part.strip()
            if not name or name in names:
                continue
            if len(name) > 20:
                raise forms.ValidationError('Тег не должен быть длиннее 20 символов.')
            names.append(name)

        if len(names) > 3:
            raise forms.ValidationError('Можно указать не более 3 тегов.')
        return names

    @transaction.atomic
    def save(self, *, author):
        self.instance.author = author
        question = super().save()

        tags = []
        for name in self.cleaned_data['tag_names']:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)

        question.tags.set(tags)
        return question


class AnswerForm(forms.ModelForm):
    text = forms.CharField(
        label='Текст ответа',
        max_length=2000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Напишите ваш ответ...',
        }),
    )

    class Meta:
        model = Answer
        fields = ('text',)

    def save(self, *, author, question):
        self.instance.author = author
        self.instance.question = question
        return super().save()


class VoteForm(forms.Form):
    value = forms.TypedChoiceField(choices=LIKE_CHOICES, coerce=int)

    @transaction.atomic
    def save(self, *, model, object_id, user):
        target = model.objects.select_for_update().get(pk=object_id)
        value = self.cleaned_data['value']

        vote, created = target.likes.get_or_create(
            user=user,
            defaults={'value': value},
        )
        if not created:
            if vote.value == value:
                raise forms.ValidationError('Вы уже так проголосовали.')
            vote.value = value
            vote.save(update_fields=['value'])

        return target.likes.aggregate(rating=Sum('value', default=0))['rating']



class CorrectAnswerForm(forms.Form):
    answer_id = forms.IntegerField(min_value=1)

    @transaction.atomic
    def save(self, *, question_id, user):
        question = Question.objects.select_for_update().get(pk=question_id)
        if question.author_id != user.pk:
            raise PermissionDenied('Выбрать правильный ответ может только автор вопроса.')

        answer = question.answers.select_for_update().get(
            pk=self.cleaned_data['answer_id'],
        )
        if not answer.is_correct:
            question.answers.filter(is_correct=True).update(is_correct=False)
            answer.is_correct = True
            answer.save(update_fields=['is_correct'])

        return answer