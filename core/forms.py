from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.core.validators import FileExtensionValidator

from .models import Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    nickname = forms.CharField(label='Никнейм', max_length=30)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'nickname')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Profile.objects.create(user=user, nickname=self.cleaned_data['nickname'])
        return user


class ProfileForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    nickname = forms.CharField(label='Никнейм', max_length=30)
    avatar = forms.ImageField(
        label='Аватар',
        required=False,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
    )

    def __init__(self, *args, user, **kwargs):
        self.user = user
        profile = getattr(user, 'profile', None)
        super().__init__(*args, initial={
            'email': user.email,
            'nickname': profile.nickname if profile else user.username,
        }, **kwargs)

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Размер файла не должен превышать 2 МБ.')
            if avatar.image.format not in ('JPEG', 'PNG'):
                raise forms.ValidationError('Выберите изображение в формате JPG или PNG.')
        return avatar

    @transaction.atomic
    def save(self):
        self.user.email = self.cleaned_data['email']
        self.user.save(update_fields=['email'])

        changes = {'nickname': self.cleaned_data['nickname']}
        if self.cleaned_data['avatar']:
            changes['avatar'] = self.cleaned_data['avatar']

        Profile.objects.update_or_create(user=self.user, defaults=changes)