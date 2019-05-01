from django import forms
from django.core.exceptions import ValidationError

from .models import Question, Answer, TakenQuiz, StudentAnswer, Quiz




class DateSelect(forms.DateInput):
    input_type = 'date'

class TimeSelect(forms.TimeInput):
    input_type = 'time'



class QuizCreateForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = ['title', 'description', 'date', 'start_time', 'end_time']
        widgets = {
            'date' : DateSelect(),
            'start_time' : TimeSelect(),
            'end_time' : TimeSelect(),
        }

class AnswerCreateForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['text', 'is_correct']

    def __init__(self, *args, **kwargs):
        super(AnswerCreateForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['style'] = 'width:75%; height:10px;'
        self.fields['is_correct'].widget.attrs['style'] = 'padding:25%;'




class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['text', ]

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['style'] = 'width:100%; height:80px;'


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answer_set.order_by('text')


