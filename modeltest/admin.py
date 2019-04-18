from django.contrib import admin
from .models import Quiz, Question, TakenQuiz
# Register your models here.

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(TakenQuiz)