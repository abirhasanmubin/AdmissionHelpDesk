from django.urls import path
from .views import CalendarView
from . import views as cl_view

urlpatterns = [
    path('index/', cl_view.index, name='index'),
    path('', CalendarView.as_view(), name='calendar'),
    path('event/new/', cl_view.event, name='event_new'),
    path('event/<int:pk>/edit/', cl_view.event, name='event_edit')
]