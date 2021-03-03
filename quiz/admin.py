from django.contrib import admin
from django.utils.safestring import mark_safe
from quiz.models import GivenHint
from quiz.models import Hint
from quiz.models import Question
from quiz.models import QuestionAnswer
from quiz.models import Quiz


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "started_at",
        "hint_penalty",
        "mistake_penalty",
    )
    search_fields = ("title",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "correct_answer",
        "quiz",
        "get_map_link",
    )
    list_filter = ("quiz",)
    search_fields = (
        "quiz__title",
        "text",
        "correct_answer",
    )
    autocomplete_fields = ("quiz",)

    def get_map_link(self, obj: Question):
        link = f'<a href="{obj.get_map_link()}">Ссылка</a>'
        return mark_safe(link)

    get_map_link.short_description = "Ссылка на карту"


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "group",
        "question",
        "text",
        "is_correct",
    )
    list_filter = (
        "group",
        "question",
    )
    search_fields = (
        "group__name",
        "question__text",
        "text",
    )
    autocomplete_fields = (
        "group",
        "question",
    )


@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "text",
    )
    list_filter = ("question",)
    search_fields = (
        "text",
        "question_text",
    )
    autocomplete_fields = ("question",)


@admin.register(GivenHint)
class GivenHintAdmin(admin.ModelAdmin):
    list_display = (
        "group",
        "hint",
    )
    list_filter = (
        "group",
        "hint",
    )
    autocomplete_fields = (
        "group",
        "hint",
    )
