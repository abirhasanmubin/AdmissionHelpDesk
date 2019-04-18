from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from pprint import pprint
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView
)
from django.views.generic.edit import FormMixin

from .models import University, AdmissionNews, Comment
from .forms import CommentForm


# Create your views here.


class UniversityListView(ListView):
    model = University
    template = 'admissionnews/university_list.html'
    context_object_name = 'universities'
    ordering = ['name']
    paginate_by = 20


class UniversityDetailView(DetailView):
    model = University

    def get_context_data(self, **kwargs):
        context = super(UniversityDetailView, self).get_context_data(**kwargs)
        uni = University.objects.filter(pk=self.kwargs.get('pk'))[0]
        context['newses'] = AdmissionNews.objects.filter(
            university=uni).order_by('-date_posted')
        return context



class UniversityCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    model = University
    fields = ['name', 'website', 'university_type', 'content', 'logo']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class UniversityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = University
    fields = ['name', 'website', 'university_type', 'content', 'logo']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        obj =self.get_object()
        if self.request.user.is_superuser or obj.user==self.request.user:
            return True
        return False


class UniversityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = University
    success_url = 'university-list'

    def test_func(self):
        uni = self.get_object()

        if self.request.user.is_superuser:
            return True
        return False

"""
"""

class AdmissionNewsListView(ListView):
    model = AdmissionNews
    template = 'admissionnews/admissionnews_list.html'
    context_object_name = 'admissionnewses'
    ordering = ['-date_posted']
    paginate_by = 5


class AdmissionNewsDetailView(FormMixin, DetailView):
    model = AdmissionNews
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(AdmissionNewsDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        post = AdmissionNews.objects.filter(pk=self.kwargs.get('pk'))[0]
        context['comments'] = Comment.objects.filter(post=post).order_by('-date_commented')
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = AdmissionNews.objects.filter(
            pk=self.kwargs.get('pk')).first()
        # comment, created = Comment.objects.get_or_create(**form.cleaned_data)
        return super().form_valid(form)

class AdmissionNewsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = AdmissionNews
    fields = ['title', 'news']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.university = University.objects.filter(
            pk=self.kwargs.get('unipk')).first()
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

class AdmissionNewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AdmissionNews
    fields = ['title', 'news']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class AdmissionNewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AdmissionNews
    success_url = 'university-list'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['comment',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = AdmissionNews.objects.filter(
            pk=self.kwargs.get('pk')).first()
        return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['comment']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = AdmissionNews.objects.filter(
            pk=self.kwargs.get('pk')).first()
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()

        if self.request.user==obj.user:
            return True
        return False

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self, **kwargs):
        return reverse_lazy('admissionnews-detail', args=(self.object.post.id,))

    def test_func(self):
        obj = self.get_object()

        if self.request.user==obj.user:
            return True
        return False