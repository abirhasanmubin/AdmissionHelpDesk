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

from eventcalendar.models import Event
from .models import University, AdmissionNews, Comment, Department
from .forms import CommentForm, AdmissionNewsCreateForm


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


    def test_func(self):
        uni = self.get_object()

        if self.request.user.is_superuser:
            return True
        return False

    def get_success_url(self):
        return reverse('university-list')

class DepartmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Department
    fields = ['name']

    def form_valid(self, form):
        form.instance.university = University.objects.filter(pk=self.kwargs.get('pk')).first()
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False

class DepartmentDetailView(DetailView):
    model =Department

class DepartmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Department
    fields = ['name']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if self.request.user.is_staff or self.request.user.is_superuser or self.request.user==obj.university.user:
            return True
        return False

class DepartmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Department

    def get_success_url(self):
        return reverse('university-detail', kwargs={'pk':self.object.university.pk})

    def test_func(self):
        obj = self.get_object()
        if self.request.user.is_staff or self.request.user.is_superuser or self.request.user==obj.university.user:
            return True
        return False


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
        title = post.title
        description = post.news
        start_time = post.start_time
        end_time = post.end_time
        Event.objects.get_or_create(title=title, description=description, start_time=start_time, end_time=end_time, admissionnews=post)
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
    form_class = AdmissionNewsCreateForm

    def form_valid(self, form):
        form.instance.university = University.objects.filter(
            pk=self.kwargs.get('unipk')).first()
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False

class AdmissionNewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AdmissionNews
    form_class = AdmissionNewsCreateForm

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False


class AdmissionNewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AdmissionNews

    def get_success_url(self):
        return reverse('university-detail', kwargs={'pk':self.object.university.pk})

    def test_func(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
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

        if self.request.user==obj.user or self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self, **kwargs):
        return reverse_lazy('admissionnews-detail', args=(self.object.post.id,))

    def test_func(self):
        obj = self.get_object()

        if self.request.user==obj.user or self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return False