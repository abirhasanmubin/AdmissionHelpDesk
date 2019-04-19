from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now

# Create your models here.

def time_now():
    now = datetime.now()
    start = now.replace(hour=20, minute=00, second=00, microsecond=00)
    return start if start > now else start + timedelta(days=1)


class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    description = models.TextField(default="")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.title




class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField(default="")

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.question.pk})



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizes = models.ManyToManyField(Quiz, through='TakenQuiz')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.question_set.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username

class TakenQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizes')
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizes')
    score = models.IntegerField()


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')