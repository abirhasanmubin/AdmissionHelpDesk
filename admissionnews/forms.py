from django.forms import ModelForm, DateInput

from .models import Comment, AdmissionNews


class CommentForm(ModelForm):

    class Meta:
        model=Comment
        fields=['comment']



class AdmissionNewsCreateForm(ModelForm):

    class Meta:
        model= AdmissionNews
        fields = ['title', 'news', 'start_time', 'end_time']
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(AdmissionNewsCreateForm, self).__init__(*args, **kwargs)
        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
