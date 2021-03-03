from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from quiz.models import GivenHint
from quiz.models import Question
from quiz.models import QuestionAnswer
from quiz.models import Quiz


class QuizDetail(DetailView):
    model = Quiz
    queryset = Quiz.objects.all()
    template_name = "quiz/quiz_detail.html"


class QuestionDetail(DetailView):
    model = Question
    queryset = Question.objects.all()
    template_name = "quiz/question_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.request.user.groups.first()
        question = self.get_object()
        answers = group.questionanswer_set.filter(question=question)
        hints = group.givenhint_set.filter(hint__question=question)
        context.update(answers=answers, hints=hints)
        return context


class QuestionAnswerCreate(LoginRequiredMixin, CreateView):
    http_method_names = ("post",)
    model = QuestionAnswer
    fields = ("text",)

    def form_valid(self, form):
        form.instance.group = self.request.user.groups.first()
        form.instance.question_id = self.kwargs.get("pk")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("quiz:question_detail", kwargs=self.kwargs)


class RequireHint(LoginRequiredMixin, DetailView):
    model = Question
    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        group = self.request.user.groups.first()
        question = self.get_object()
        hints = question.hint_set.all().values_list("id")
        given_hints = group.givenhint_set.filter(hint__question=question).values_list("hint_id")

        for hint_id in hints:
            if hint_id not in given_hints:
                GivenHint.objects.create(group=group, hint_id=hint_id)
                break
        else:
            messages.error(request, "Больше нет подсказок по этому вопросу!")
        return redirect("quiz:question_detail", pk=question.id)


class ResultsList(DetailView):
    template_name = "quiz/results.html"
    model = Quiz
    queryset = Quiz.objects.all()

    def get_score(self, group: Group):
        quiz = self.get_object()
        correct_answer_count, penalty = 0, 0
        for question in quiz.question_set.all():
            answers = group.questionanswer_set.filter(question=question)
            total_answers = answers.count()
            total_hints = group.givenhint_set.filter(hint__question=question).count()
            correct_answer = None
            for answer in answers:
                if answer.is_correct:
                    correct_answer = answer
                    break

            if correct_answer is not None:
                correct_answer_count += 1
                question_penalty = (
                    correct_answer.time_spent.seconds
                    + (total_answers - 1) * quiz.mistake_penalty
                    + total_hints * quiz.hint_penalty
                )
                penalty += question_penalty

        return correct_answer_count, penalty

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Group.objects.all()
        data_groups = []
        for group in groups:
            correct_answer_count, penalty = self.get_score(group)
            data_group = {"name": group.name, "correct_answer_count": correct_answer_count, "penalty": penalty}
            data_groups.append(data_group)

        def key_func(item):
            return -item["correct_answer_count"], item["penalty"]

        context["groups"] = sorted(data_groups, key=key_func)
        return context
