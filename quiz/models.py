from urllib.parse import urlencode

from django.db import models


class Quiz(models.Model):
    class Meta:
        verbose_name = "игра"
        verbose_name_plural = "игры"

    title = models.CharField(verbose_name="название", max_length=128)
    started_at = models.DateTimeField(verbose_name="время начала игры")
    mistake_penalty = models.IntegerField(verbose_name="штраф за ошибку (в секундах)")
    hint_penalty = models.IntegerField(verbose_name="штраф за подсказку (в секундах)")

    def __str__(self):
        return self.title


class Question(models.Model):
    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"

    quiz = models.ForeignKey("Quiz", models.CASCADE, verbose_name="игра")
    text = models.TextField(verbose_name="текст", max_length=1024)
    correct_answer = models.TextField(verbose_name="правильный ответ", max_length=256)

    longitude = models.FloatField(verbose_name="долгота")
    latitude = models.FloatField(verbose_name="широта")

    def __str__(self):
        return self.text

    def get_map_link(self):
        params = {
            "ll": f"{self.longitude},{self.latitude}",
            "z": 15,
            "pt": f"{self.longitude},{self.latitude}",
        }
        return "https://yandex.ru/maps/?" + urlencode(params)


class QuestionAnswer(models.Model):
    class Meta:
        verbose_name = "ответ на вопрос"
        verbose_name_plural = "ответы на вопросы"

    group = models.ForeignKey("auth.Group", models.CASCADE, verbose_name="команда")
    question = models.ForeignKey("Question", models.CASCADE, verbose_name="вопрос")
    text = models.TextField(verbose_name="текст", max_length=1024)
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True, editable=False)

    @property
    def is_correct(self):
        return self.question.correct_answer == self.text

    @property
    def time_spent(self):
        return self.created_at - self.question.quiz.started_at

    def __str__(self):
        return f"{self.group.name}: {self.text}"


class Hint(models.Model):
    class Meta:
        verbose_name = "подсказка"
        verbose_name_plural = "подсказки"

    question = models.ForeignKey("Question", models.CASCADE, verbose_name="вопрос")
    text = models.TextField(verbose_name="текст", max_length=1024)


class GivenHint(models.Model):
    class Meta:
        verbose_name = "данная подсказка"
        verbose_name_plural = "данные подсказки"
        unique_together = ("group", "hint")

    group = models.ForeignKey("auth.Group", models.CASCADE, verbose_name="команда")
    hint = models.ForeignKey("Hint", models.CASCADE, verbose_name="подсказка")
