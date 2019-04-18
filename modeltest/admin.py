from django.contrib import admin
from .models import Quiz, Question, TakenQuiz, Student, StudentAnswer
# Register your models here.

admin.site.register(Quiz)
admin.site.register(StudentAnswer)
admin.site.register(Student)
admin.site.register(Question)
admin.site.register(TakenQuiz)