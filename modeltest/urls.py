from django.urls import path
from .views import (
    QuizCreateView, QuizDetailView, QuizListView,
    QuizUpdateView, QuizDeleteView,
    QuestionCreateView, QuestionUpdateView, QuestionDetailView,
    QuestionListView, QuestionDeleteView,
    AnswerCreateView, AnswerDetailView,
    AnswerDeleteView, AnswerUpdateView,

    TakenQuizListView,
)
import modeltest.views as mt_view

urlpatterns = [
    path('quiz/', QuizListView.as_view(), name='quiz-list'),
    path('quiz/new/', QuizCreateView.as_view(), name='quiz-create'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name="quiz-detail"),
    path('quiz/<int:pk>/update/', QuizUpdateView.as_view(), name="quiz-update"),
    path('quiz/<int:pk>/delete/', QuizDeleteView.as_view(), name="quiz-delete"),

    path('quiz/<int:pk>/question/', QuestionListView.as_view(), name='question-list'),
    path('quiz/<int:pk>/question/new/', QuestionCreateView.as_view(), name='question-create'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/', mt_view.Question_Change, name='question-detail'),
    path('quiz/question/<int:pk>/update/', QuestionUpdateView.as_view(), name='question-update'),
    path('quiz/question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question-delete'),

    path('quiz/question/<int:pk>/answer/new/', AnswerCreateView.as_view(), name='answer-create'),
    path('quiz/answer/<int:pk>/', AnswerDetailView.as_view(), name='answer-detail'),
    path('quiz/answer/<int:pk>/update/', AnswerUpdateView.as_view(), name='answer-update'),
    path('quiz/answer/<int:pk>/delete/', AnswerDeleteView.as_view(), name='answer-delete'),
    # path('quiz/<int:quiz_pk>/question/<int:question_pk)>/', mt_view.Question_Change, name='question-change')

    path('student/quiz/<int:pk>/', mt_view.take_quiz, name='take-quiz'),
    path('student/<int:pk>/quiz/', TakenQuizListView.as_view(), name='taken-quiz')
]