from django.contrib import admin
from django.db.models import Exists, OuterRef

from .models import Answer, AnswerLike, Question, QuestionLike, Tag


class TagUsageFilter(admin.SimpleListFilter):
    title = 'использование в вопросах'
    parameter_name = 'used'

    def lookups(self, request, model_admin):
        return (('yes', 'Используются'), ('no', 'Не используются'))

    def queryset(self, request, queryset):
        if self.value() in ('yes', 'no'):
            questions = Question.tags.through.objects.filter(tag_id=OuterRef('pk'))
            return queryset.alias(in_use=Exists(questions)).filter(in_use=self.value() == 'yes')
        return queryset


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
    list_filter = (TagUsageFilter,)
    ordering = ('name',)


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ('author', 'text', 'is_correct', 'created_at')
    readonly_fields = fields
    show_change_link = True
    can_delete = False
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'text', 'author__username')
    list_filter = ('created_at',)
    list_select_related = ('author',)
    autocomplete_fields = ('author', 'tags')
    ordering = ('-created_at', '-pk')
    inlines = (AnswerInline,)
    show_full_result_count = False


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'author', 'is_correct', 'created_at')
    search_fields = ('text', 'question__title', 'author__username')
    list_filter = ('is_correct', 'created_at')
    list_select_related = ('question', 'author')
    autocomplete_fields = ('question', 'author')
    show_full_result_count = False


@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'value')
    search_fields = ('user__username', 'question__title')
    list_filter = ('value',)
    list_select_related = ('user', 'question')
    autocomplete_fields = ('user', 'question')
    show_full_result_count = False


@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'answer', 'value')
    search_fields = ('user__username', 'answer__text', 'answer__question__title')
    list_filter = ('value',)
    list_select_related = ('user', 'answer')
    autocomplete_fields = ('user', 'answer')
    show_full_result_count = False