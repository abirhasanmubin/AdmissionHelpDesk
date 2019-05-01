from time import timezone

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from pprint import pprint
from datetime import datetime
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView
)
from django.views.generic.edit import FormMixin
from django.db import transaction
from django.db.models import Avg, Count
from .forms import QuestionForm, TakeQuizForm, BaseAnswerInlineFormSet, QuizCreateForm

from .models import Quiz, TakenQuiz, Question, Answer, StudentAnswer, Student
# Create your views here.


class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    context_object_name = 'quizes'
    paginate_by = 10
    ordering = ['-date', 'start_time']


class QuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz

    def get_context_data(self, **kwargs):
        context = super(QuizDetailView, self).get_context_data(**kwargs)
        quiz = Quiz.objects.filter(pk=self.kwargs.get('pk'))[0]
        context['questions'] = Question.objects.filter(quiz=quiz).order_by('-pk')
        return context


class QuizCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Quiz
    form_class = QuizCreateForm

    def get_success_url(self):
        return reverse('quiz-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False

class QuizUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Quiz
    form_class = QuizCreateForm

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        obj =self.get_object()
        if self.request.user.is_superuser or self.request.user.is_staff or obj.user==self.request.user:
            return True
        return False

class QuizDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Quiz

    def get_success_url(self):
        return reverse('quiz-list')

    def test_func(self):
        obj =self.get_object()
        if self.request.user.is_superuser or self.request.user.is_staff or obj.user==self.request.user:
            return True
        return False

class QuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Question
    fields = ['text']

    def form_valid(self, form):
        form.instance.quiz = Quiz.objects.filter(pk=self.kwargs.get('pk')).first()
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False

    def get_success_url(self):
        return reverse('question-detail', kwargs={'question_pk': self.object.pk, 'quiz_pk': self.object.quiz.pk})

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    fields = ['text']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if self.request.user.is_superuser or self.request.user.is_staff or obj.quiz.user==self.request.user:
            return True
        return False


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = 'questions'
    paginate_by = 1

    def get_queryset(self):
        quiz = Quiz.objects.filter(pk=self.kwargs.get('pk'))[0]
        return Question.objects.filter(quiz=quiz)

class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        question = Question.objects.filter(pk=self.kwargs.get('pk'))[0]
        context['answers'] = Answer.objects.filter(question=question)
        return context

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question

    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False

    def get_success_url(self):
        return reverse('quiz-detail', kwargs={'pk':self.object.quiz.pk})


class AnswerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Answer
    fields = ['text', 'is_correct']

    def form_valid(self, form):
        form.instance.question = Question.objects.filter(pk=self.kwargs.get('pk')).first()
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False

class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    fields = ['text', 'is_correct']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        ob = self.get_object()
        if self.request.user.is_superuser or self.request.user.is_staff or ob.question.quiz.user==self.request.user:
            return True
        return False

class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer


    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False

    def get_success_url(self):
        return reverse('question-detail', kwargs={'pk': self.object.question.pk})

class AnswerDetailView(LoginRequiredMixin, DetailView):
    model = Answer

@login_required
def Question_Change(request, quiz_pk, question_pk):
    if not request.user.is_staff and not request.user.is_superuser:
        return render(request, 'admissionnews/forbidden.html')

    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=4,
        validate_min=True,
        max_num=5,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('question-detail', question_pk=question.pk, quiz_pk=quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'modeltest/question_change_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })


class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizes'
    template_name = 'modeltest/taken_quiz.html'

    def get_queryset(self):
        quiz = Quiz.objects.filter(pk=self.kwargs.get('pk'))
        queryset = TakenQuiz.objects.values()
        return queryset

def get_time(end, start):
    t1 = end.hour*60+end.minute
    t2 = start.hour*60+start.minute
    return t1-t2


class TakenExamListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Quiz
    context_object_name = 'taken_list'
    template_name = 'modeltest/taken_quiz_list.html'

    def get_queryset(self):
        quiz = Quiz.objects.filter(pk=self.kwargs.get('pk')).first()
        queryset = TakenQuiz.objects.filter(quiz=quiz).all()
        return queryset

    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False



@login_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student
    date = datetime.now().strftime('%d:%m:%Y')
    t_date = quiz.date.strftime('%d:%m:%Y')
    t_now = datetime.now()
    now = datetime.now().strftime('%H:%M')
    start = quiz.start_time.strftime('%H:%M')
    t_start = quiz.start_time
    end = quiz.end_time.strftime('%H:%M')
    t_end = quiz.end_time

    if t_date<date:
        return render(request, 'modeltest/ended.html')
    if t_date==date:
        if start>now:
            return render(request, 'modeltest/upcoming.html')
        if end<now:
            return render(request, 'modeltest/ended.html')
    if t_date>date and now>end:
        return render(request, 'modeltest/upcoming.html')

    if student.quizes.filter(pk=pk).exists():
        return render(request, 'modeltest/taken_quiz.html')

    total_questions = quiz.question_set.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()

    progress = 100 - (get_time(t_end, t_now)/get_time(t_end, t_start)) * 100
    question = unanswered_questions.first()

    if request.method == 'POST':
        if t_date == date:
            if start > now:
                return render(request, 'modeltest/ended.html')
            if end <= now:
                return render(request, 'modeltest/ended.html')

        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                quiz_answer = form.save(commit=False)
                quiz_answer.student = student
                quiz_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('take-quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = correct_answers
                    score_p = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(user=student, quiz=quiz, score=score)
                    if score_p < 40.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s points out of %s points.' % (quiz.title, score, quiz.question_set.count()))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points out of %s points.' % (quiz.title, score, quiz.question_set.count()))
                    return redirect('quiz-list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'modeltest/taken_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })