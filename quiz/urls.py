from django.urls import path
from quiz.views import QuestionAnswerCreate
from quiz.views import QuestionDetail
from quiz.views import QuizDetail
from quiz.views import RequireHint

app_name = "quiz"

urlpatterns = [
    path("<int:pk>/", QuizDetail.as_view(), name="quiz_detail"),
    path("questions/<int:pk>/", QuestionDetail.as_view(), name="question_detail"),
    path("questions/<int:pk>/answer/", QuestionAnswerCreate.as_view(), name="answer"),
    path("questions/<int:pk>/require_hint/", RequireHint.as_view(), name="require_hint"),
]
