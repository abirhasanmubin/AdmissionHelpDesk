from django.urls import path
from .views import CalendarView, EventCreate
from . import views as cl_view

urlpatterns = [
    path('index/', cl_view.index, name='index'),
    path('', CalendarView.as_view(), name='calendar'),
    path('event/<int:pk>/new/', EventCreate.as_view(), name='event-new'),
]